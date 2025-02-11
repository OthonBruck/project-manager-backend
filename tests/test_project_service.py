import pytest
from unittest.mock import AsyncMock
from services.project_service import ProjectService
from schemas.project import ProjectCreate

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
