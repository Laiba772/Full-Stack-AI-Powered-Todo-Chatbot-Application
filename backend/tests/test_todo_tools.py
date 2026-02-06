from uuid import UUID, uuid4
from datetime import datetime
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from fastapi import HTTPException

from src.tools.todo_tools import add_task_handler, list_tasks_handler, update_task_handler, complete_task_handler, delete_task_handler
from src.schemas.task import AddTaskInput, TaskOutput, ListTasksOutput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput, StatusOutput
from src.api.errors import TaskNotFoundException
from src.models.task import Task # Import Task model


@pytest.fixture
def mock_task_service():
    """Fixture for a mocked TaskService."""
    with patch('src.services.task_service.TaskService', autospec=True) as MockTaskService:
        instance = MockTaskService.return_value
        
        # Mock verify_task_ownership to return an actual Task object or None
        # This is needed because the real update_task and complete_task call this
        mock_task = MagicMock(spec=Task) # Create a mock Task object
        mock_task.id = uuid4()
        mock_task.user_id = uuid4()
        mock_task.title = "Mock Task Title"
        mock_task.description = "Mock Task Description"
        mock_task.is_complete = False
        mock_task.created_at = datetime.utcnow()
        mock_task.updated_at = datetime.utcnow()

        instance.verify_task_ownership = AsyncMock(return_value=mock_task)
        
        yield instance





@pytest.fixture
def test_user_id():
    """Fixture for a test user UUID."""
    return uuid4()


@pytest.mark.asyncio
async def test_add_task_handler(mock_task_service, test_user_id):
    task_input = AddTaskInput(title="Buy milk", description="Buy milk")
    expected_output = TaskOutput(id=uuid4(), title="Buy milk", description="Buy milk", is_complete=False)
    mock_task_service.create_task.return_value = expected_output

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    result = await add_task_handler(task_input, test_user_id, mock_task_service, mock_tool_service)

    mock_task_service.create_task.assert_called_once_with(test_user_id, task_input)
    assert result == expected_output


@pytest.mark.asyncio
async def test_list_tasks_handler(mock_task_service, test_user_id):
    task1 = TaskOutput(id=uuid4(), title="Task 1", description="Task 1", is_complete=False)
    task2 = TaskOutput(id=uuid4(), title="Task 2", description="Task 2", is_complete=True)
    expected_tasks = [task1, task2]
    mock_task_service.get_tasks.return_value = expected_tasks

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    result = await list_tasks_handler(test_user_id, None, mock_task_service, mock_tool_service)

    mock_task_service.get_tasks.assert_called_once_with(test_user_id, None)
    assert result == ListTasksOutput(items=expected_tasks)

    # Test with filter
    mock_task_service.get_tasks.reset_mock()
    mock_task_service.get_tasks.return_value = [task1]
    result_filtered = await list_tasks_handler(test_user_id, False, mock_task_service, mock_tool_service)
    mock_task_service.get_tasks.assert_called_once_with(test_user_id, False)
    assert result_filtered == ListTasksOutput(items=[task1])


@pytest.mark.asyncio
async def test_update_task_handler(mock_task_service, test_user_id):
    update_input = UpdateTaskInput(task_id=uuid4(), description="Updated description")
    expected_output = TaskOutput(id=update_input.task_id, title="Updated Title", description="Updated description", is_complete=False)
    mock_task_service.update_task.return_value = expected_output

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    result = await update_task_handler(update_input, test_user_id, mock_task_service, mock_tool_service)

    mock_task_service.update_task.assert_called_once_with(test_user_id, update_input)
    assert result == expected_output


@pytest.mark.asyncio
async def test_update_task_handler_not_found(mock_task_service, test_user_id):
    update_input = UpdateTaskInput(task_id=uuid4(), description="Updated description")
    mock_task_service.update_task.return_value = None

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    with pytest.raises(TaskNotFoundException):
        await update_task_handler(update_input, test_user_id, mock_task_service, mock_tool_service)


@pytest.mark.asyncio
async def test_complete_task_handler(mock_task_service, test_user_id):
    complete_input = CompleteTaskInput(task_id=uuid4())
    mock_task_service.complete_task.return_value = True

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    result = await complete_task_handler(complete_input, test_user_id, mock_task_service, mock_tool_service)

    mock_task_service.complete_task.assert_called_once_with(test_user_id, complete_input.task_id)
    assert result == StatusOutput(task_id=complete_input.task_id, status="completed")


@pytest.mark.asyncio
async def test_complete_task_handler_not_found(mock_task_service, test_user_id):
    complete_input = CompleteTaskInput(task_id=uuid4())
    mock_task_service.complete_task.return_value = False

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    with pytest.raises(TaskNotFoundException):
        await complete_task_handler(complete_input, test_user_id, mock_task_service, mock_tool_service)


@pytest.mark.asyncio
async def test_delete_task_handler(mock_task_service, test_user_id):
    delete_input = DeleteTaskInput(task_id=uuid4())
    mock_task_service.delete_task.return_value = True

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    result = await delete_task_handler(delete_input, test_user_id, mock_task_service, mock_tool_service)

    mock_task_service.delete_task.assert_called_once_with(test_user_id, delete_input.task_id)
    assert result == StatusOutput(task_id=delete_input.task_id, status="deleted")


@pytest.mark.asyncio
async def test_delete_task_handler_not_found(mock_task_service, test_user_id):
    delete_input = DeleteTaskInput(task_id=uuid4())
    mock_task_service.delete_task.return_value = False

    # Mock the tool invocation service as well
    mock_tool_service = AsyncMock()

    with pytest.raises(TaskNotFoundException):
        await delete_task_handler(delete_input, test_user_id, mock_task_service, mock_tool_service)
