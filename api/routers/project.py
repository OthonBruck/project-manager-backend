from fastapi import APIRouter, Depends, status, BackgroundTasks
from schemas.project import ProjectCreate, ProjectResponseCreate, ProjectResponseGet, ProjectAddMember
from schemas.api_response import ApiResponse
from services.project_service import ProjectService
from services.notification_service import NotificationService
from utils.security import get_current_user
from utils.functions import get_service

router = APIRouter()

@router.post("/", response_model=ApiResponse[ProjectResponseCreate], status_code=status.HTTP_201_CREATED)
async def register_project(project: ProjectCreate, service=Depends(get_service(ProjectService)), current_user=Depends(get_current_user)):
    project_response = await service.create_project(project, current_user)
    return {"message": "Projeto criado com sucesso", "data": project_response}

@router.get("/{id}", response_model=ApiResponse[ProjectResponseGet], status_code=status.HTTP_200_OK)
async def get_project(id, service=Depends(get_service(ProjectService)), current_user=Depends(get_current_user)):
    project_response = await service.get_project_by_id(id)
    return {"message": "Projeto encontrado com sucesso", "data": project_response}

@router.patch("/{project_id}/members", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def add_member(project_id, member: ProjectAddMember, background_tasks: BackgroundTasks, service=Depends(get_service(ProjectService)), notification_service=Depends(get_service(NotificationService)), current_user=Depends(get_current_user)):
    await service.add_member_to_project(project_id, member, notification_service, current_user, background_tasks)
    return {"message": "Usuário autenticado com sucesso"}