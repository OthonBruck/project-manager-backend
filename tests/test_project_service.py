import pytest
from unittest.mock import AsyncMock
from services.project_service import ProjectService
from schemas.project import ProjectCreate
from utils.functions import serialize_document, serialize_list
from bson import ObjectId
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_create_project():
    mock_collection = AsyncMock()

    mock_insert_result = AsyncMock()
    mock_collection.insert_one.return_value = mock_insert_result

    mock_db = AsyncMock()
    mock_db.get_collection = AsyncMock(return_value=mock_collection)

    service = ProjectService(mock_db)

    project_data = ProjectCreate(title="Projeto Teste", description="Descrição do projeto")
    current_user = {"id": "user123"}

    result = await service.create_project(project_data, current_user)

    assert result["title"] == "Projeto Teste"
    assert result["description"] == "Descrição do projeto"
    assert result["owner"] == current_user

    mock_collection.insert_one.assert_called_once_with({
        "title": "Projeto Teste",
        "description": "Descrição do projeto",
        "owner": current_user,
        "members": []
    })

@pytest.mark.asyncio
async def test_get_project_by_id():
    fake_project_id = str(ObjectId())

    mock_db = AsyncMock()
    mock_collection = AsyncMock()

    fake_project = {
        "_id": ObjectId(fake_project_id),
        "title": "Projeto Teste",
        "description": "Descrição do projeto",
        "owner": "user123",
        "members": []
    }

    mock_db.get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = fake_project

    service = ProjectService(mock_db)

    result = await service.get_project_by_id(fake_project_id)

    assert result == serialize_document(fake_project)

    mock_db.get_collection.assert_called_once_with("project")
    mock_collection.find_one.assert_called_once_with({"_id": ObjectId(fake_project_id)})

@pytest.mark.asyncio
async def test_get_project_by_id_not_found():
    fake_project_id = str(ObjectId())

    mock_db = AsyncMock()
    mock_collection = AsyncMock()

    mock_db.get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = None

    service = ProjectService(mock_db)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_project_by_id(fake_project_id)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Project does not exist."

@pytest.mark.asyncio
async def test_get_project_visible_by_user():
    mock_db = AsyncMock()
    mock_collection = AsyncMock()

    mock_db.get_collection.return_value = mock_collection

    mock_collection.find.return_value.to_list = AsyncMock(return_value=[
        {"_id": "project1", "owner": "user123", "members": [{"user_id": "user456"}]},
        {"_id": "project2", "owner": "user789", "members": [{"user_id": "user123"}]}
    ])

    service = ProjectService(mock_db)

    result = await service.get_project_visible_by_user("user123")

    assert len(result) == 2
    assert result[0]["owner"] == "user123"
    assert result[1]["members"][0]["user_id"] == "user123"

    mock_collection.find.assert_called_once_with({
        "$or": [
            {"owner": "user123"},
            {"members.user_id": "user123"}
        ]
    })

@pytest.mark.asyncio
async def test_get_project_by_id_not_found():
    fake_project_id = str(ObjectId())

    mock_db = AsyncMock()
    mock_collection = AsyncMock()

    mock_db.get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = None

    service = ProjectService(mock_db)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_project_by_id(fake_project_id)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Project does not exist."