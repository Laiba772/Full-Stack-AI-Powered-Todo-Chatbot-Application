from fastapi import APIRouter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.main import MCPServer

from src.tools.todo_tools import add_task_handler, list_tasks_handler, update_task_handler, complete_task_handler, delete_task_handler, incomplete_task_handler
from src.schemas.task import TaskOutput, ListTasksOutput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput, StatusOutput


# This router will hold the MCP tool definitions as API endpoints
# In a real MCP SDK, this might be handled internally by the SDK
# For now, we'll simulate the registration
router = APIRouter()

def register_mcp_tools(mcp_server_instance: 'MCPServer'): # Accept mcp_server_instance as argument
    """
    Function to register MCP tools with the MCP server.
    Actual tool definitions (e.g., add_task, list_tasks) would be
    registered as API endpoints on the mcp_server.app here.
    """
    mcp_server_instance.app.post("/add_task", response_model=TaskOutput)(add_task_handler)
    mcp_server_instance.app.get("/list_tasks", response_model=ListTasksOutput)(list_tasks_handler)
    mcp_server_instance.app.post("/update_task", response_model=TaskOutput)(update_task_handler)
    mcp_server_instance.app.post("/complete_task", response_model=StatusOutput)(complete_task_handler)
    mcp_server_instance.app.post("/delete_task", response_model=StatusOutput)(delete_task_handler)
    mcp_server_instance.app.post("/incomplete_task", response_model=StatusOutput)(incomplete_task_handler)
    mcp_server_instance.app.get("/status", response_model=StatusOutput)(
        lambda: StatusOutput(status="MCP tools are registered and operational.")
    )


def get_openai_tool_schemas(mcp_server_instance: 'MCPServer') -> list[dict]:
    """
    Extracts registered tool schemas from the MCP server's FastAPI app
    and converts them into the format expected by OpenAI for function calling.
    """
    openapi_schema = mcp_server_instance.app.openapi()
    tools = []
    
    # Filter out paths that are not MCP tools or are status/health checks
    # Assuming MCP tools are POST requests with a specific structure
    # and not GET requests unless they have specific input schemas
    for path, path_item in openapi_schema.get("paths", {}).items():
        for method, operation in path_item.items():
            # Only consider POST methods for now for actions, and GET for specific queries
            # Exclude /status
            if method.lower() in ["post", "get"] and path != "/status":
                # Extract tool name from path, removing leading/trailing underscores and the method
                path_parts = path.strip('/').split('/')
                # Take the first part of the path as the tool name (e.g., "add_task" from "/add_task")
                tool_name = path_parts[0] if path_parts and path_parts[0] else path.replace("/", "_").strip("_")
                
                # If there's a requestBody, it's a POST tool
                if "requestBody" in operation:
                    content = operation["requestBody"].get("content", {})
                    if "application/json" in content:
                        schema_ref = content["application/json"].get("schema", {}).get("$ref")
                        if schema_ref:
                            schema_name = schema_ref.split("/")[-1]
                            json_schema = openapi_schema["components"]["schemas"][schema_name]
                            
                            # OpenAI expects "properties" and "required" directly in the schema
                            properties = json_schema.get("properties", {})
                            required = json_schema.get("required", [])

                            tools.append({
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "description": operation.get("description") or operation.get("summary"),
                                    "parameters": {
                                        "type": "object",
                                        "properties": properties,
                                        "required": required,
                                    },
                                },
                            })
                # If it's a GET request with parameters, it's also a tool
                elif "parameters" in operation:
                    # Collect query parameters for GET requests
                    properties = {}
                    required = []
                    for param in operation["parameters"]:
                        if param["in"] == "query":
                            properties[param["name"]] = param["schema"]
                            if param.get("required"):
                                required.append(param["name"])
                    
                    if properties: # Only add if there are actual query parameters
                        # For GET requests, ensure we use the path-based tool name
                        get_tool_name = path_parts[0] if path_parts and path_parts[0] else path.replace("/", "_").strip("_")
                        tools.append({
                            "type": "function",
                            "function": {
                                "name": get_tool_name,
                                "description": operation.get("description") or operation.get("summary"),
                                "parameters": {
                                    "type": "object",
                                    "properties": properties,
                                    "required": required,
                                },
                            },
                        })
    return tools

# Call this function during application startup (e.g., in main.py's lifespan event)
# to ensure tools are registered.
