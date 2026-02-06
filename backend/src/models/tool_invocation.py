"""Tool invocation tracking model for MCP server."""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
import json


class ToolInvocation(SQLModel, table=True):
    """Tool invocation tracking entity for monitoring and debugging.

    Attributes:
        id: Unique tool invocation identifier (UUID)
        user_id: Foreign key to the User who invoked the tool
        tool_name: Name of the invoked tool (e.g., 'add_task', 'list_tasks')
        parameters: JSON representation of the parameters passed to the tool
        result: JSON representation of the tool's result
        success: Boolean indicating if the tool invocation was successful
        timestamp: Timestamp of when the tool was invoked
        error_message: Optional error message if the tool invocation failed
    """

    __tablename__ = "tool_invocations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True)
    tool_name: str = Field(index=True)
    parameters: str = Field(default="{}")  # Store as JSON string
    result: Optional[str] = Field(default=None)  # Store as JSON string
    success: bool = Field(default=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = Field(default=None, max_length=500)

    def set_parameters(self, params: Dict[str, Any]) -> None:
        """Helper method to set parameters as JSON string."""
        self.parameters = json.dumps(params, default=str)

    def get_parameters(self) -> Dict[str, Any]:
        """Helper method to get parameters as dictionary."""
        return json.loads(self.parameters)

    def set_result(self, result: Any) -> None:
        """Helper method to set result as JSON string."""
        if result is not None:
            self.result = json.dumps(result, default=str)

    def get_result(self) -> Optional[Any]:
        """Helper method to get result as original type."""
        if self.result is not None:
            return json.loads(self.result)
        return None

    def __repr__(self) -> str:
        return (
            f"<ToolInvocation id={self.id} user_id={self.user_id} "
            f"tool_name='{self.tool_name}' success={self.success}>"
        )