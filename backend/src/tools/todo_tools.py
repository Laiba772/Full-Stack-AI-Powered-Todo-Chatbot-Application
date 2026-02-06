from typing import Optional
from fastapi import Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.models.database import get_async_session
from src.core.auth import get_current_user_id_from_token
from src.services.task_service import TaskService
from src.services.tool_invocation_service import ToolInvocationService
from src.schemas.task import AddTaskInput, TaskOutput, ListTasksOutput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput, StatusOutput
from src.api.errors import TaskNotFoundException
import logging

logger = logging.getLogger(__name__)


def get_task_service(session: AsyncSession = Depends(get_async_session)) -> TaskService:
    """Dependency that provides a TaskService instance."""
    return TaskService(session)


def get_tool_invocation_service(session: AsyncSession = Depends(get_async_session)) -> ToolInvocationService:
    """Dependency that provides a ToolInvocationService instance."""
    return ToolInvocationService(session)


async def add_task_handler(
    task_input: AddTaskInput,
    user_id: UUID = Depends(get_current_user_id_from_token),
    task_service: TaskService = Depends(get_task_service),
    tool_service: ToolInvocationService = Depends(get_tool_invocation_service)
) -> TaskOutput:
    """
    Handles the `add_task` MCP tool invocation.
    Creates a new todo task for the authenticated user.
    """
    logger.info(f"User {user_id} attempting to add task: {task_input.title}")
    try:
        result = await task_service.create_task(user_id, task_input)
        logger.info(f"User {user_id} successfully added task {result.id}")

        # Log the successful tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="add_task",
            parameters=task_input.model_dump(),
            success=True,
            result=result.model_dump() if hasattr(result, 'model_dump') else result.dict() if hasattr(result, 'dict') else result
        )

        return result
    except Exception as e:
        logger.error(f"Error adding task for user {user_id}: {e}", exc_info=True)

        # Log the failed tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="add_task",
            parameters=task_input.model_dump(),
            success=False,
            error_message=str(e)
        )

        raise # Re-raise to be caught by global exception handler


async def list_tasks_handler(
    user_id: UUID = Depends(get_current_user_id_from_token),
    is_complete: Optional[bool] = None,
    task_service: TaskService = Depends(get_task_service),
    tool_service: ToolInvocationService = Depends(get_tool_invocation_service)
) -> ListTasksOutput:
    """
    Handles the `list_tasks` MCP tool invocation.
    Retrieves a list of todo tasks for the authenticated user,
    optionally filtered by completion status.
    """
    logger.info(f"User {user_id} attempting to list tasks (is_complete={is_complete})")
    try:
        tasks = await task_service.get_tasks(user_id, is_complete)
        logger.info(f"User {user_id} retrieved {len(tasks)} tasks.")

        # Log the successful tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="list_tasks",
            parameters={"is_complete": is_complete},
            success=True,
            result={"count": len(tasks)}
        )

        return ListTasksOutput(tasks=tasks, page=1)  # Include page field as required by schema
    except Exception as e:
        logger.error(f"Error listing tasks for user {user_id}: {e}", exc_info=True)

        # Log the failed tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="list_tasks",
            parameters={"is_complete": is_complete},
            success=False,
            error_message=str(e)
        )

        raise # Re-raise to be caught by global exception handler


async def update_task_handler(
    task_input: UpdateTaskInput,
    user_id: UUID = Depends(get_current_user_id_from_token),
    task_service: TaskService = Depends(get_task_service),
    tool_service: ToolInvocationService = Depends(get_tool_invocation_service)
) -> TaskOutput:
    """
    Handles the `update_task` MCP tool invocation.
    Updates an existing todo task for the authenticated user.
    """
    logger.info(f"User {user_id} attempting to update task {task_input.task_id} with {task_input.model_dump(exclude_unset=True)}")
    try:
        updated_task = await task_service.update_task(user_id, task_input)
        if not updated_task:
            logger.warning(f"Update failed: Task {task_input.task_id} not found or not owned by user {user_id}.")
            raise TaskNotFoundException(task_id=task_input.task_id) # Use custom exception
        logger.info(f"User {user_id} successfully updated task {task_input.task_id}")

        # Log the successful tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="update_task",
            parameters=task_input.model_dump(),
            success=True,
            result=updated_task.model_dump() if hasattr(updated_task, 'model_dump') else updated_task.dict() if hasattr(updated_task, 'dict') else updated_task
        )

        return updated_task
    except Exception as e:
        logger.error(f"Error updating task {task_input.task_id} for user {user_id}: {e}", exc_info=True)

        # Log the failed tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="update_task",
            parameters=task_input.model_dump(),
            success=False,
            error_message=str(e)
        )

        raise


async def complete_task_handler(
    task_input: CompleteTaskInput,
    user_id: UUID = Depends(get_current_user_id_from_token),
    task_service: TaskService = Depends(get_task_service),
    tool_service: ToolInvocationService = Depends(get_tool_invocation_service)
) -> StatusOutput:
    """
    Handles the `complete_task` MCP tool invocation.
    Marks a todo task as complete for the authenticated user.
    """
    logger.info(f"User {user_id} attempting to complete task {task_input.task_id}")
    try:
        success = await task_service.complete_task(user_id, task_input.task_id)
        if not success:
            logger.warning(f"Complete failed: Task {task_input.task_id} not found or not owned by user {user_id}.")
            raise TaskNotFoundException(task_id=task_input.task_id) # Use custom exception
        logger.info(f"User {user_id} successfully completed task {task_input.task_id}")

        # Log the successful tool invocation
        result_status = StatusOutput(task_id=task_input.task_id, status="completed")
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="complete_task",
            parameters=task_input.model_dump(),
            success=True,
            result=result_status.model_dump() if hasattr(result_status, 'model_dump') else result_status.dict() if hasattr(result_status, 'dict') else result_status
        )

        return result_status
    except Exception as e:
        logger.error(f"Error completing task {task_input.task_id} for user {user_id}: {e}", exc_info=True)

        # Log the failed tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="complete_task",
            parameters=task_input.model_dump(),
            success=False,
            error_message=str(e)
        )

        raise


async def delete_task_handler(
    task_input: DeleteTaskInput,
    user_id: UUID = Depends(get_current_user_id_from_token),
    task_service: TaskService = Depends(get_task_service),
    tool_service: ToolInvocationService = Depends(get_tool_invocation_service)
) -> StatusOutput:
    """
    Handles the `delete_task` MCP tool invocation.
    Deletes a todo task for the authenticated user.
    """
    logger.info(f"User {user_id} attempting to delete task {task_input.task_id}")
    try:
        success = await task_service.delete_task(user_id, task_input.task_id)
        if not success:
            logger.warning(f"Delete failed: Task {task_input.task_id} not found or not owned by user {user_id}.")
            raise TaskNotFoundException(task_id=task_input.task_id) # Use custom exception
        logger.info(f"User {user_id} successfully deleted task {task_input.task_id}")

        # Log the successful tool invocation
        result_status = StatusOutput(task_id=task_input.task_id, status="deleted")
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="delete_task",
            parameters=task_input.model_dump(),
            success=True,
            result=result_status.model_dump() if hasattr(result_status, 'model_dump') else result_status.dict() if hasattr(result_status, 'dict') else result_status
        )

        return result_status
    except Exception as e:
        logger.error(f"Error deleting task {task_input.task_id} for user {user_id}: {e}", exc_info=True)

        # Log the failed tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="delete_task",
            parameters=task_input.model_dump(),
            success=False,
            error_message=str(e)
        )

        raise


async def incomplete_task_handler(
    task_input: CompleteTaskInput, # Reusing CompleteTaskInput as it only needs task_id
    user_id: UUID = Depends(get_current_user_id_from_token),
    task_service: TaskService = Depends(get_task_service),
    tool_service: ToolInvocationService = Depends(get_tool_invocation_service)
) -> StatusOutput:
    """
    Handles the `incomplete_task` MCP tool invocation.
    Marks a todo task as incomplete for the authenticated user.
    """
    logger.info(f"User {user_id} attempting to mark task {task_input.task_id} as incomplete")
    try:
        # Call update_task with is_complete=False
        updated_task = await task_service.update_task(user_id, UpdateTaskInput(
            task_id=task_input.task_id,
            is_complete=False
        ))
        if not updated_task:
            logger.warning(f"Incomplete failed: Task {task_input.task_id} not found or not owned by user {user_id}.")
            raise TaskNotFoundException(task_id=task_input.task_id)
        logger.info(f"User {user_id} successfully marked task {task_input.task_id} as incomplete")

        # Log the successful tool invocation
        result_status = StatusOutput(task_id=task_input.task_id, status="incomplete")
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="incomplete_task",
            parameters=task_input.model_dump(),
            success=True,
            result=result_status.model_dump() if hasattr(result_status, 'model_dump') else result_status.dict() if hasattr(result_status, 'dict') else result_status
        )

        return result_status
    except Exception as e:
        logger.error(f"Error marking task {task_input.task_id} as incomplete for user {user_id}: {e}", exc_info=True)

        # Log the failed tool invocation
        await tool_service.log_tool_invocation(
            user_id=user_id,
            tool_name="incomplete_task",
            parameters=task_input.model_dump(),
            success=False,
            error_message=str(e)
        )

        raise