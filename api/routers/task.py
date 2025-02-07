from fastapi import APIRouter, Depends, status
from schemas.task import TaskCreate, TaskResponseCreate, TaskResponseGet, TaskUpdate
from schemas.api_response import ApiResponse
from services.task_service import TaskService
from utils.security import get_current_user
from utils.functions import get_service

router = APIRouter()

@router.post("/", response_model=ApiResponse[TaskResponseCreate], status_code=status.HTTP_201_CREATED)
async def register_task(task: TaskCreate, service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    task_response = await service.create_task(task)
    return {"message": "Tarefa criada com sucesso", "data": task_response}

@router.get("/{id}", response_model=ApiResponse[TaskResponseGet], status_code=status.HTTP_200_OK)
async def get_task(id, service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    task_response = await service.get_task_by_id(id)
    return {"message": "Tarefa encontrada com sucesso", "data": task_response}

#TODO: Ajustar retorno
@router.patch("/{id}", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def update_task(id, task_data: TaskUpdate, service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    task_response = await service.update_task_by_id(id, task_data)
    return {"message": "Tarefa atualizada com sucesso"}
