from fastapi import APIRouter, Depends, status
from schemas.project import ProjectCreate, ProjectResponseCreate, ProjectResponseGet
from schemas.api_response import ApiResponse
from services.project_service import ProjectService
from db.database import get_database

router = APIRouter()

@router.post("/", response_model=ApiResponse[ProjectResponseCreate], status_code=status.HTTP_201_CREATED)
async def register_project(project: ProjectCreate, db=Depends(get_database)):
    project_response = await ProjectService.create_project(project, db)
    return {"message": "Projeto criado com sucesso", "data": project_response}

@router.get("/{id}", response_model=ApiResponse[ProjectResponseGet], status_code=status.HTTP_200_OK)
async def get_project(id, db=Depends(get_database)):
    project_response = await ProjectService.get_project_by_id(id, db)
    return {"message": "Projeto encontrado com sucesso", "data": project_response}
