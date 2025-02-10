from schemas.task import TaskCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document, check_permission, serialize_list
from datetime import datetime, timedelta, timezone

class TaskService:
    def __init__(self, db):
        self.db = db.get_collection("task")

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
        await self.db.insert_one(new_task)

        return new_task

    async def get_task_by_id(self, id):
        result = await self.db.find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        return serialize_document(result)

    async def get_tasks_by_project(self, project_id):
        result = await self.db.find({"project_id": ObjectId(project_id)})
        if not result:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        return serialize_list(result)
    
    async def update_task_by_id(self, task_id, task_data, current_user):
        task = await self.db.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        project = await check_permission(str(task.get("project_id")), ["admin", "editor"], current_user)

        update_data = task_data.model_dump(exclude_none=True)
        
        await self.db.update_one(
                {"_id": ObjectId(task_id)}, 
                {
                    "$set": update_data
                }
            )
        return {}

    async def delete_task(self, task_id, current_user):
        task = await self.db.find_one({"_id": ObjectId(task_id)})
        project = await check_permission(str(task.get("project_id")), ["admin", "editor"], current_user)
        if not project:
            raise HTTPException(status_code=400, detail="Project does not exist.")
        
        await self.db.delete_one({"_id": ObjectId(task_id)})
        return True
