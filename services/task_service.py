from schemas.task import TaskCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document

class TaskService:
    def __init__(self, db):
        self.db = db
    
    async def create_task(self, task_data: TaskCreate):
        new_task = {
            "title": task_data.title,
            "description": task_data.description,
        }
        await self.db.get_collection("task").insert_one(new_task)

        return new_task

    async def get_task_by_id(self, id):
        result = await self.db.get_collection("task").find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        return serialize_document(result)