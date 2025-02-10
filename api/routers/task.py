from fastapi import APIRouter, Depends, status
from schemas.task import TaskCreate, TaskResponseCreate, TaskResponseGet, TaskUpdate
from schemas.api_response import ApiResponse
from services.task_service import TaskService
from utils.security import get_current_user
from utils.functions import get_service
from typing import List

router = APIRouter()

@router.post("/", response_model=ApiResponse[TaskResponseCreate], status_code=status.HTTP_201_CREATED)
async def register_task(task: TaskCreate, service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    task_response = await service.create_task(task, current_user)
    return {"message": "Tarefa criada com sucesso", "data": task_response}

@router.get("/{task_id}", response_model=ApiResponse[TaskResponseGet], status_code=status.HTTP_200_OK)
async def get_task(task_id, service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    task_response = await service.get_task_by_id(task_id)
    return {"message": "Tarefa encontrada com sucesso", "data": task_response}

@router.get("/{project_id}/tasks", response_model=ApiResponse[List[TaskResponseGet]], status_code=status.HTTP_200_OK)
async def get_projects_tasks(service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    task_response = await service.get_tasks_by_project(current_user)
    return {"message": "Tarefas encontradas com sucesso", "data": task_response}

@router.patch("/{task_id}", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def update_task(task_id, task_data: TaskUpdate, service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    await service.update_task_by_id(task_id, task_data, current_user)
    return {"message": "Tarefa atualizada com sucesso"}

@router.delete("/{task_id}", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def add_member(task_id, service=Depends(get_service(TaskService)), current_user=Depends(get_current_user)):
    await service.delete_task(task_id, current_user)
    return {"message": "Tarefa removido com sucesso"}