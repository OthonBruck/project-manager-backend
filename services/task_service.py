from schemas.task import TaskCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document, check_permission, serialize_list
from datetime import datetime, timedelta, timezone
from repository.task_repository import TaskRepository

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task_data: TaskCreate, current_user):
        project = await check_permission(task_data.project_id, ["admin", "editor"], current_user)
        new_task = {
            "project_id": ObjectId(task_data.project_id),
            "title": task_data.title,
            "description": task_data.description,
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
            "created_by": current_user,
            "updated_at": datetime.now(timezone.utc),
        }
        await self.repository.create(new_task)

        return new_task

    async def get_task_by_id(self, id):
        result = await self.repository.find_by_id(id)
        if not result:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        return serialize_document(result)

    async def get_tasks_by_project(self, project_id):
        result = await self.repository.find_by_project_id(project_id)
        if not result:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        return serialize_list(result)
    
    async def update_task_by_id(self, task_id, task_data, current_user):
        task = await self.repository.find_by_id({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        project = await check_permission(str(task.get("project_id")), ["admin", "editor"], current_user)

        update_data = task_data.model_dump(exclude_none=True)
        
        await self.repository.update_by_id(task_id, update_data)
        return {}

    async def delete_task(self, task_id, current_user):
        task = await self.repository.find_by_id({"_id": ObjectId(task_id)})
        project = await check_permission(str(task.get("project_id")), ["admin", "editor"], current_user)
        if not project:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        
        await self.repository.delete_by_id(task_id)
        return True
