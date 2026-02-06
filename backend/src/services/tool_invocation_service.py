"""Service layer for tool invocation tracking."""
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.models.tool_invocation import ToolInvocation


class ToolInvocationService:
    """Service for managing tool invocation tracking."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_tool_invocation(
        self,
        user_id: UUID,
        tool_name: str,
        parameters: Dict[str, Any],
        success: bool = True,
        result: Optional[Any] = None,
        error_message: Optional[str] = None
    ) -> ToolInvocation:
        """Log a tool invocation to the database.

        Args:
            user_id: The UUID of the user invoking the tool
            tool_name: The name of the tool being invoked
            parameters: The parameters passed to the tool
            success: Whether the tool invocation was successful
            result: The result of the tool invocation (if successful)
            error_message: The error message if the tool invocation failed

        Returns:
            The created ToolInvocation record
        """
        invocation = ToolInvocation(
            user_id=user_id,
            tool_name=tool_name,
            success=success,
            error_message=error_message
        )
        
        invocation.set_parameters(parameters)
        if success and result is not None:
            invocation.set_result(result)

        self.session.add(invocation)
        await self.session.commit()
        await self.session.refresh(invocation)

        return invocation

    async def get_user_tool_history(
        self,
        user_id: UUID,
        tool_name: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[ToolInvocation]:
        """Get tool invocation history for a specific user.

        Args:
            user_id: The UUID of the user
            tool_name: Optional tool name to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of ToolInvocation records
        """
        query = select(ToolInvocation).where(ToolInvocation.user_id == user_id)

        if tool_name:
            query = query.where(ToolInvocation.tool_name == tool_name)

        query = query.order_by(ToolInvocation.timestamp.desc()).offset(offset).limit(limit)

        result = await self.session.exec(query)
        return result.all()

    async def get_recent_invocations(
        self,
        limit: int = 100
    ) -> list[ToolInvocation]:
        """Get recent tool invocations across all users.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of recent ToolInvocation records
        """
        query = select(ToolInvocation).order_by(ToolInvocation.timestamp.desc()).limit(limit)
        result = await self.session.exec(query)
        return result.all()