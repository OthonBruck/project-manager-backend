import pytest
from unittest.mock import AsyncMock, patch
from services.project_service import ProjectService
from schemas.project import ProjectCreate, ProjectAddMember, ProjectDictAddMember
from utils.functions import serialize_document, serialize_list
from bson import ObjectId
from fastapi import HTTPException
from typing import List

@pytest.mark.asyncio
async def test_create_project():
    mock_repository = AsyncMock()
    mock_repository.create.return_value = {
        "_id": "fake_project_id",
        "title": "Projeto Teste",
        "description": "Descrição do projeto",
        "owner": "user123",
        "members": []
    }

    service = ProjectService(mock_repository)

    project_data = ProjectCreate(title="Projeto Teste", description="Descrição do projeto")
    current_user = "user123"

    result = await service.create_project(project_data, current_user)

    assert result["title"] == "Projeto Teste"
    assert result["description"] == "Descrição do projeto"
    assert result["owner"] == "user123"
    assert "fake_project_id" in str(result["_id"])

    mock_repository.create.assert_called_once_with({
        "title": "Projeto Teste",
        "description": "Descrição do projeto",
        "owner": "user123",
        "members": []
    })

@pytest.mark.asyncio
async def test_get_project_by_id():
    fake_project_id = str(ObjectId())

    mock_repository = AsyncMock()

    fake_project = {
        "_id": ObjectId(fake_project_id),
        "title": "Projeto Teste",
        "description": "Descrição do projeto",
        "owner": "user123",
        "members": []
    }
    mock_repository.find_by_id.return_value = fake_project

    service = ProjectService(mock_repository)
    result = await service.get_project_by_id(fake_project_id)

    assert result == serialize_document(fake_project)

    mock_repository.find_by_id.assert_called_once_with(fake_project_id)

@pytest.mark.asyncio
async def test_get_project_by_id_not_found():
    fake_project_id = str(ObjectId())

    mock_repository = AsyncMock()

    mock_repository.find_by_id.return_value = None

    service = ProjectService(mock_repository)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_project_by_id(fake_project_id)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Project does not exist."

@pytest.mark.asyncio
async def test_get_project_visible_by_user():
    fake_project_id = str(ObjectId())
    mock_repository = AsyncMock()

    mock_repository.find_projects_by_user.return_value = [
            {
            "_id": ObjectId(fake_project_id),
            "title": "Projeto Teste",
            "description": "Descrição do projeto",
            "owner": "user123",
            "members": []
        }
    ]

    service = ProjectService(mock_repository)

    result = await service.get_project_visible_by_user("user123")

    assert len(result) == 1
    assert result[0]["owner"] == "user123"

    mock_repository.find_projects_by_user.assert_called_once_with("user123")

@pytest.mark.asyncio
async def test_find_projects_by_user_not_found():
    fake_project_id = str(ObjectId())

    mock_repository = AsyncMock()

    mock_repository.find_projects_by_user.return_value = None

    service = ProjectService(mock_repository)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_project_visible_by_user(fake_project_id)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "No projects to display."

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_update_project_by_id_success(mock_check_permission):
    mock_check_permission.return_value = True

    mock_repo = AsyncMock()
    mock_repo.find_by_id.return_value = {
        "_id": "project123",
        "title": "Projeto Antigo"
    }
    mock_repo.update_by_id.return_value.modified_count = 1
    mock_repo.find_by_id.return_value = {
        "_id": "project123",
        "title": "Projeto Atualizado"
    }

    service = ProjectService(mock_repo)
    
    project_data = ProjectCreate(title="Projeto Atualizado", description="projeto")
    current_user = {"id": "user123"}

    result = await service.update_project_by_id("project123", project_data, current_user)

    assert result["title"] == "Projeto Atualizado"
    mock_repo.update_by_id.assert_called_once_with("project123", {"title": "Projeto Atualizado",  "description": "projeto"})

@pytest.mark.asyncio
async def test_update_project_by_id_project_not_found():
    mock_repo = AsyncMock()
    mock_repo.find_by_id.return_value = None

    service = ProjectService(mock_repo)

    project_data = ProjectCreate(title="Projeto Atualizado", description="projeto")
    current_user = {"id": "user123"}

    with pytest.raises(HTTPException) as excinfo:
        await service.update_project_by_id("invalid_id", project_data, current_user)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Project does not exist."

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_update_project_by_id_no_permission(mock_check_permission):
    mock_check_permission.side_effect = HTTPException(status_code=403, detail="Not authorized")

    mock_repo = AsyncMock()
    mock_repo.find_by_id.return_value = {"_id": "project123"}

    service = ProjectService(mock_repo)

    project_data = ProjectCreate(title="Projeto Atualizado", description="projeto")
    current_user = {"id": "user123"}

    with pytest.raises(HTTPException) as excinfo:
        await service.update_project_by_id("project123", project_data, current_user)

    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "Not authorized"

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_update_project_by_id_no_valid_fields(mock_check_permission):
    mock_check_permission.return_value = True

    mock_repo = AsyncMock()
    mock_repo.find_by_id.return_value = {"_id": "project123"}

    service = ProjectService(mock_repo)

    project_data = ProjectCreate()
    current_user = {"id": "user123"}

    with pytest.raises(HTTPException) as excinfo:
        await service.update_project_by_id("project123", project_data, current_user)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "No valid fields to update."

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_update_project_by_id_no_changes(mock_check_permission):
    mock_check_permission.return_value = True

    mock_repo = AsyncMock()
    mock_repo.find_by_id.return_value = {
        "_id": "project123",
        "title": "Projeto Antigo"
    }
    mock_repo.update_by_id.return_value.modified_count = 0

    service = ProjectService(mock_repo)

    project_data = ProjectCreate(title="Projeto Atualizado", description="projeto")
    current_user = {"id": "user123"}

    with pytest.raises(HTTPException) as excinfo:
        await service.update_project_by_id("project123", project_data, current_user)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "No changes were made."

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_add_member_to_project_success(mock_check_permission):
    # Mock do projeto existente e permissão concedida
    mock_check_permission.return_value = {
        "_id": "project123",
        "title": "Projeto Teste",
        "members": [{"user_id": "user456"}]
    }

    # Mock do repositório e serviços
    mock_repo = AsyncMock()
    mock_notification_service = AsyncMock()
    mock_background_tasks = AsyncMock()

    service = ProjectService(mock_repo)

    # Usando o Pydantic para criar o membro
    member_data = ProjectAddMember(users_id=[{"user_id": "user789", "role": "editor"}])
    current_user = {"id": "user123"}

    result = await service.add_member_to_project(
        project_id="project123", 
        member=member_data, 
        notification_service=mock_notification_service, 
        current_user=current_user, 
        background_tasks=mock_background_tasks
    )

    assert result["message"] == "User added to project"
    mock_repo.update_members_by_id.assert_called_once_with("project123", [{"user_id": "user789", "role": "editor"}])
    mock_background_tasks.add_task.assert_called()

# ----------------------------------------------

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_add_member_to_project_project_not_found(mock_check_permission):
    # Mock do projeto não encontrado (None) ou sem permissão
    mock_check_permission.return_value = None

    mock_repo = AsyncMock()
    mock_notification_service = AsyncMock()
    mock_background_tasks = AsyncMock()

    service = ProjectService(mock_repo)

    member_data = ProjectAddMember(users_id=[{"user_id": "user789", "role": "editor"}])
    current_user = {"id": "user123"}

    with pytest.raises(HTTPException) as excinfo:
        await service.add_member_to_project(
            project_id="invalid_project", 
            member=member_data, 
            notification_service=mock_notification_service, 
            current_user=current_user, 
            background_tasks=mock_background_tasks
        )

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Project does not exist."

# ----------------------------------------------

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_add_member_to_project_user_already_member(mock_check_permission):
    # Mock do projeto existente com o usuário já como membro
    mock_check_permission.return_value = {
        "_id": "project123",
        "title": "Projeto Teste",
        "members": [{"user_id": "user789"}]
    }

    mock_repo = AsyncMock()
    mock_notification_service = AsyncMock()
    mock_background_tasks = AsyncMock()

    service = ProjectService(mock_repo)

    member_data = ProjectAddMember(users_id=[{"user_id": "user789", "role": "editor"}])  # Membro já existe
    current_user = {"id": "user123"}

    with pytest.raises(HTTPException) as excinfo:
        await service.add_member_to_project(
            project_id="project123", 
            member=member_data, 
            notification_service=mock_notification_service, 
            current_user=current_user, 
            background_tasks=mock_background_tasks
        )

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "User is already a member"

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_delete_project_success(mock_check_permission):
    mock_check_permission.return_value = {
        "_id": "project123",
        "title": "Projeto Teste",
        "members": [{"user_id": "user456"}]
    }

    mock_repo = AsyncMock()

    service = ProjectService(mock_repo)

    current_user = {"id": "user123"}

    result = await service.delete_project(
        project_id="project123", 
        current_user=current_user, 
    )

    assert result == True
    mock_repo.delete_by_id.assert_called_once_with("project123")

@pytest.mark.asyncio
@patch("services.project_service.check_permission")
async def test_delete_project_error(mock_check_permission):
    mock_check_permission.return_value = None

    mock_repo = AsyncMock()

    service = ProjectService(mock_repo)

    current_user = {"id": "user123"}
    with pytest.raises(HTTPException) as excinfo:
        result = await service.delete_project(
            project_id="project123", 
            current_user=current_user, 
        )

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Project does not exist."