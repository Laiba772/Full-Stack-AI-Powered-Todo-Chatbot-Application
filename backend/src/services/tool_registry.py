from typing import Dict, Type, Optional, List
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    Base abstract class for all AI agent tools.
    """
    name: str
    description: str

    @abstractmethod
    async def run(self, **kwargs):
        """
        Executes the tool's functionality.
        """
        pass

class ToolRegistry:
    """
    Manages the registration and retrieval of AI agent tools.
    """
    _tools: Dict[str, Type[BaseTool]] = {}

    @classmethod
    def register_tool(cls, tool_class: Type[BaseTool]):
        """
        Registers an AI agent tool.
        """
        if not issubclass(tool_class, BaseTool):
            raise ValueError(f"Tool must inherit from BaseTool: {tool_class.__name__}")
        cls._tools[tool_class.name] = tool_class

    @classmethod
    def get_tool(cls, name: str) -> Optional[Type[BaseTool]]:
        """
        Retrieves a registered tool by its name.
        """
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls) -> List[Dict[str, str]]:
        """
        Lists all registered tools with their names and descriptions.
        """
        return [{"name": tool.name, "description": tool.description} for tool in cls._tools.values()]
