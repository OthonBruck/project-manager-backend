from schemas.task import TaskCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document

class TaskService:
    @staticmethod
    async def create_task(task_data: TaskCreate, db):
        new_task = {
            "title": task_data.title,
            "description": task_data.description,
        }
        await db.get_collection("task").insert_one(new_task)

        return new_task

    async def get_task_by_id(id, db):
        result = await db.get_collection("task").find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        return serialize_document(result)