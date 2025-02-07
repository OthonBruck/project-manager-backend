from schemas.task import TaskCreate
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document
from datetime import datetime, timedelta, timezone

class TaskService:
    def __init__(self, db):
        self.db = db.get_collection("task")
    
    async def create_task(self, task_data: TaskCreate):
        new_task = {
            "title": task_data.title,
            "description": task_data.description,
            "status": "uncompleted",
            "created_at": datetime.now(timezone.utc)
        }
        await self.db.insert_one(new_task)

        return new_task

    async def get_task_by_id(self, id):
        result = await self.db.find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        return serialize_document(result)
    
    #TODO: Find a better way to handle if there is a None in task_data
    async def update_task_by_id(self, task_id, task_data):
        task = await self.db.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=400, detail="Task does not exist.")
        
        add_task = {}
        if task_data.title and task_data.title != None:
            add_task["title"] = task_data.title
        if task_data and task_data.description != None:
            add_task["description"] = task_data.description
        if task_data and task_data.status!= None:
            add_task["status"] = task_data.status
        
        await self.db.update_one(
                {"_id": ObjectId(task_id)}, 
                {
                    "$set": add_task
                }
            )
        return {}