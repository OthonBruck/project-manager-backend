from fastapi import APIRouter, Depends, status
from schemas.task import TaskCreate, TaskResponseCreate, TaskResponseGet
from schemas.api_response import ApiResponse
from services.task_service import TaskService
from db.database import get_database

router = APIRouter()

@router.post("/", response_model=ApiResponse[TaskResponseCreate], status_code=status.HTTP_201_CREATED)
async def register_task(task: TaskCreate, db=Depends(get_database)):
    task_response = await TaskService.create_task(task, db)
    return {"message": "Tarefa criada com sucesso", "data": task_response}

@router.get("/{id}", response_model=ApiResponse[TaskResponseGet], status_code=status.HTTP_200_OK)
async def get_task(id, db=Depends(get_database)):
    task_response = await TaskService.get_task_by_id(id, db)
    return {"message": "Tarefa encontrada com sucesso", "data": task_response}
