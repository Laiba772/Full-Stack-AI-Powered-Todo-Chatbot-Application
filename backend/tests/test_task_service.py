from uuid import uuid4
from datetime import datetime, timedelta
import pytest
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.pool import StaticPool
from typing import AsyncGenerator
import os

from src.models.user import User
from src.models.task import Task
from src.services.task_service import TaskService
from src.schemas.task import AddTaskInput, UpdateTaskInput




@pytest.fixture(name="task_service")
async def task_service_fixture(session: AsyncSession) -> TaskService: # Expect AsyncSession
    return TaskService(session)


@pytest.fixture(name="test_user")
async def test_user_fixture(session: AsyncSession) -> User:
    """Create a test user with hashed password."""
    user_uuid = uuid4()
    user = User(
        username=f"testuser_{user_uuid.hex}", # Make username unique
        email=f"test_{user_uuid}@example.com",
        password_hash="hashed_password"
    )
    session.add(user)
    # No commit or refresh here; let the outer transaction in conftest.py handle it.
    return user


@pytest.mark.asyncio
async def test_create_task(task_service: TaskService, test_user: User):
    task_input = AddTaskInput(title="Test Task", description="Test task", due_date=datetime.utcnow() + timedelta(days=1))
    new_task = await task_service.create_task(test_user.id, task_input)

    assert new_task.id is not None
    assert new_task.description == "Test task"
    assert new_task.is_complete is False
    assert (await task_service.verify_task_ownership(test_user.id, new_task.id)) is not None


@pytest.mark.asyncio
async def test_get_tasks(task_service: TaskService, test_user: User):
    # Create some tasks for the test user
    task1_input = AddTaskInput(title="Task 1", description="Task 1")
    task2_input = AddTaskInput(title="Task 2", description="Task 2")
    task1 = await task_service.create_task(test_user.id, task1_input)
    task2 = await task_service.create_task(test_user.id, task2_input)

    # Test get all tasks
    all_tasks = await task_service.get_tasks(test_user.id)
    assert len(all_tasks) == 2

    # Test get incomplete tasks
    incomplete_tasks = await task_service.get_tasks(test_user.id, is_complete=False)
    assert len(incomplete_tasks) == 2 # Initially both are incomplete
    assert all(not t.is_complete for t in incomplete_tasks)

    # Test get complete tasks (should be 0 initially)
    complete_tasks = await task_service.get_tasks(test_user.id, is_complete=True)
    assert len(complete_tasks) == 0

    # Mark one task complete and retest
    await task_service.complete_task(test_user.id, task1.id)
    complete_tasks = await task_service.get_tasks(test_user.id, is_complete=True)
    assert len(complete_tasks) == 1
    assert complete_tasks[0].id == task1.id


@pytest.mark.asyncio
async def test_update_task(task_service: TaskService, test_user: User):
    task_input = AddTaskInput(title="Original Task", description="Original task")
    original_task = await task_service.create_task(test_user.id, task_input)

    update_input = UpdateTaskInput(task_id=original_task.id, description="Updated task", is_complete=True)
    updated_task = await task_service.update_task(test_user.id, update_input)

    assert updated_task is not None
    assert updated_task.description == "Updated task"
    assert updated_task.is_complete is True


@pytest.mark.asyncio
async def test_update_task_not_owned(task_service: TaskService, test_user: User, different_user: User):
    task_input = AddTaskInput(title="Other Task", description="Other user's task")
    other_task = await task_service.create_task(different_user.id, task_input)

    update_input = UpdateTaskInput(task_id=other_task.id, description="Attempted update")
    updated_task = await task_service.update_task(test_user.id, update_input) # Try to update other user's task

    assert updated_task is None


@pytest.mark.asyncio
async def test_complete_task(task_service: TaskService, test_user: User):
    task_input = AddTaskInput(title="Complete Task", description="Task to complete")
    task = await task_service.create_task(test_user.id, task_input)
    assert task.is_complete is False

    success = await task_service.complete_task(test_user.id, task.id)
    assert success is True

    updated_task = await task_service.verify_task_ownership(test_user.id, task.id)
    assert updated_task.is_complete is True


@pytest.mark.asyncio
async def test_complete_task_not_owned(task_service: TaskService, test_user: User, different_user: User):
    task_input = AddTaskInput(title="Other Task", description="Other user's task to complete")
    other_task = await task_service.create_task(different_user.id, task_input)

    success = await task_service.complete_task(test_user.id, other_task.id)
    assert success is False


@pytest.mark.asyncio
async def test_delete_task(task_service: TaskService, test_user: User):
    task_input = AddTaskInput(title="Delete Task", description="Task to delete")
    task = await task_service.create_task(test_user.id, task_input)
    assert (await task_service.verify_task_ownership(test_user.id, task.id)) is not None

    success = await task_service.delete_task(test_user.id, task.id)
    assert success is True

    assert (await task_service.verify_task_ownership(test_user.id, task.id)) is None


@pytest.mark.asyncio
async def test_delete_task_not_owned(task_service: TaskService, test_user: User, different_user: User):
    task_input = AddTaskInput(title="Other Task", description="Other user's task to delete")
    other_task = await task_service.create_task(different_user.id, task_input)

    success = await task_service.delete_task(test_user.id, other_task.id)
    assert success is False
