from bson import ObjectId

class TaskRepository:
    def __init__(self, db):
        self.collection = db.get_collection("task")

    async def create(self, task_data: dict):
        result = await self.collection.insert_one(task_data)
        return str(result.inserted_id)
    
    async def find_by_id(self, task_id: str):
        task = await self.collection.find_one({"_id": ObjectId(task_id)})
        return task

    async def find_by_project_id(self, project_id: str):
        task = await self.collection.find({"project_id": ObjectId(project_id)})
        return task.to_list()
    
    async def update_by_id(self, task_id: str, update_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        return result
    async def delete_by_id(self, task_id: str):
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        return result