from typing import List, Dict, Any, Optional, Tuple
import json
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message, Sender
from src.config import settings
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall

from src.services.tool_registry import ToolRegistry, BaseTool

class AIAgentService:
    """
    Service for interacting with the AI agent, including tool invocation.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.available_tools = {tool_name: tool_class for tool_name, tool_class in ToolRegistry._tools.items()}

    async def _process_tool_calls(
        self, tool_calls: List[ChatCompletionMessageToolCall]
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Processes and executes tool calls made by the AI agent.

        Returns:
            A tuple containing:
            - List of tool call details (for storing in Message model).
            - List of tool output details (for storing in Message model and feeding back to AI).
        """
        tool_call_details = []
        tool_outputs = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            tool_call_details.append({
                "id": tool_call.id,
                "function": {"name": function_name, "arguments": tool_call.function.arguments}
            })

            tool_output_item = {
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": ""
            }

            if function_name in self.available_tools:
                tool_to_run = self.available_tools[function_name](self.session)
                try:
                    result = await tool_to_run.run(**function_args)
                    tool_output_item["content"] = str(result)
                except Exception as tool_e:
                    tool_output_item["content"] = f"Tool {function_name} failed: {str(tool_e)}"
            else:
                tool_output_item["content"] = f"Error: Tool {function_name} not found."
            
            tool_outputs.append(tool_output_item)
        
        return tool_call_details, tool_outputs


    async def generate_response(
        self, user: User, conversation: Conversation, messages: List[Message], user_message: str
    ) -> Tuple[str, Optional[List[Dict]], Optional[List[Dict]]]:
        """
        Generates a response from the AI agent, potentially involving tool calls.

        Args:
            user: The authenticated user.
            conversation: The current conversation.
            messages: List of previous messages in the conversation.
            user_message: The current message from the user.

        Returns:
            A tuple containing:
            - The AI agent's response as a string.
            - Optional list of tool calls made by the AI.
            - Optional list of tool outputs from executed tools.
        """
        initial_messages_for_ai = [{"role": "system", "content": settings.ai_agent_system_prompt}]

        for msg in messages:
            if msg.tool_calls:
                # Reconstruct tool_calls for OpenAI format
                # Ensure each tool_call has 'id', 'function'
                tool_calls_openai_format = [{
                    "id": tc["id"],
                    "function": {"name": tc["function"]["name"], "arguments": tc["function"]["arguments"]}
                } for tc in msg.tool_calls]
                initial_messages_for_ai.append({"role": "assistant", "tool_calls": tool_calls_openai_format})
            
            if msg.tool_output:
                for tool_output_item in msg.tool_output:
                    # Reconstruct tool_output for OpenAI format
                    initial_messages_for_ai.append({
                        "role": "tool",
                        "tool_call_id": tool_output_item["tool_call_id"],
                        "name": tool_output_item["name"],
                        "content": tool_output_item["content"]
                    })
            
            if not msg.tool_calls and not msg.tool_output: # Only add content if it's a regular message
                 initial_messages_for_ai.append({"role": msg.sender.value, "content": msg.content})


        # Add the current user message
        initial_messages_for_ai.append({"role": Sender.USER.value, "content": user_message})

        full_response_messages = list(initial_messages_for_ai)

        ai_response_content = None
        final_tool_calls: Optional[List[Dict]] = None
        final_tool_outputs: Optional[List[Dict]] = None

        try:
            while True:
                response = await self.client.chat.completions.create(
                    model=settings.openai_agent_model,
                    messages=full_response_messages,
                    tools=[
                        {
                            "type": "function",
                            "function": {
                                "name": tool_class.name,
                                "description": tool_class.description,
                                "parameters": tool_class.parameters,
                            },
                        }
                        for tool_class in self.available_tools.values()
                    ],
                    tool_choice="auto",
                    max_tokens=settings.openai_agent_max_tokens,
                    temperature=0.7,
                    user=str(user.id)
                )

                response_message = response.choices[0].message
                full_response_messages.append(response_message)

                if response_message.tool_calls:
                    final_tool_calls, tool_outputs_from_execution = await self._process_tool_calls(response_message.tool_calls)
                    final_tool_outputs = tool_outputs_from_execution # Store these for the final return

                    # Append tool outputs to full_response_messages for the next AI turn
                    for output in tool_outputs_from_execution:
                        full_response_messages.append(
                            {"tool_call_id": output["tool_call_id"], "role": "tool", "name": output["name"], "content": output["content"]}
                        )
                else:
                    ai_response_content = response_message.content
                    break # Exit loop if AI provides a textual response

            return ai_response_content, final_tool_calls, final_tool_outputs

        except Exception as e:
            return f"Error communicating with AI agent: {str(e)}", None, None