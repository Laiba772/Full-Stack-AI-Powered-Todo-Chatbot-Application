from typing import Dict, Any
from src.services.tool_registry import BaseTool
from sqlmodel.ext.asyncio.session import AsyncSession # Assuming tools might need session

class EchoTool(BaseTool):
    name = "echo_tool"
    description = "Echoes back the input text. Useful for testing tool invocation."
    parameters = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to echo back."
            }
        },
        "required": ["text"]
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def run(self, text: str) -> Dict[str, Any]:
        return {"echoed_text": text}