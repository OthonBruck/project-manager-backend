import pytest
from unittest.mock import AsyncMock, patch
from services.task_service import TaskService
from schemas.task import TaskCreate, TaskUpdate
from utils.functions import serialize_document, serialize_list
from bson import ObjectId
from fastapi import HTTPException
from typing import List
from datetime import datetime, timezone

@pytest.mark.asyncio
@patch("services.task_service.check_permission")
async def test_create_task_success(mock_check_permission):
    mock_check_permission.return_value = True
    fake_project_id = str(ObjectId())
    mock_repository = AsyncMock()
    date = datetime.now(timezone.utc)
    mock_repository.create.return_value =  {
        "project_id":"fake_project_id",
        "description":"description",
        "title": "title",
    }

    service = TaskService(mock_repository)

    task_data = TaskCreate(project_id=fake_project_id, description="description", title="title",)

    result = await service.create_task(task_data, "user_id")

    assert result["project_id"] == ObjectId(fake_project_id)

@pytest.mark.asyncio
async def test_get_task_by_id_success():
    fake_task_id = str(ObjectId())

    mock_repository = AsyncMock()

    fake_task = {
        "_id": ObjectId(fake_task_id),
        "project_id": "project_id",
        "title": "task",
        "description": "Descrição da task",
    }
    mock_repository.find_by_id.return_value = fake_task

    service = TaskService(mock_repository)
    result = await service.get_task_by_id(fake_task_id)

    assert result == serialize_document(fake_task)

    mock_repository.find_by_id.assert_called_once_with(fake_task_id)

@pytest.mark.asyncio
async def test_get_tasks_by_project_success():
    fake_task_id = str(ObjectId())
    fake_project_id = str(ObjectId())

    mock_repository = AsyncMock()

    fake_task = [{
        "_id": ObjectId(fake_task_id),
        "project_id": fake_project_id,
        "title": "task",
        "description": "Descrição da task",
    }]
    mock_repository.find_by_project_id.return_value = fake_task

    service = TaskService(mock_repository)
    result = await service.get_tasks_by_project(fake_project_id)

    assert result == serialize_list(fake_task)

    mock_repository.find_by_project_id.assert_called_once_with(fake_project_id)


@pytest.mark.asyncio
@patch("services.task_service.check_permission")
async def test_update_task_by_id_success(mock_check_permission):
    mock_check_permission.return_value = True
    fake_task_id = str(ObjectId())
    fake_project_id = str(ObjectId())

    mock_repository = AsyncMock()

    fake_task = {
        "_id": ObjectId(fake_task_id),
        "project_id": fake_project_id,
        "title": "task",
        "description": "Descrição da task",
        "status": "uncompleted"
    }
    
    mock_repository.find_by_id.return_value = fake_task
    mock_repository.update_by_id.return_value = True

    update_data = TaskUpdate(title="teste", description="description", status="completed")

    service = TaskService(mock_repository)
    result = await service.update_task_by_id(fake_task_id, update_data, "user_id")

    assert result == {}

    mock_repository.update_by_id.assert_called_once_with(str(fake_task_id), {"title": "teste", "description": "description", "status": "completed"})

@pytest.mark.asyncio
@patch("services.task_service.check_permission")
async def test_delete_task_success(mock_check_permission):
    mock_check_permission.return_value = True
    fake_task_id = str(ObjectId())
    fake_project_id = str(ObjectId())

    mock_repository = AsyncMock()

    fake_task = {
        "_id": ObjectId(fake_task_id),
        "project_id": fake_project_id,
        "title": "task",
        "description": "Descrição da task",
        "status": "uncompleted"
    }
    
    mock_repository.find_by_id.return_value = fake_task
    mock_repository.delete_by_id.return_value = True

    service = TaskService(mock_repository)
    result = await service.delete_task(fake_task_id, "user_id")

    assert result == True

    mock_repository.delete_by_id.assert_called_once_with(fake_task_id)
