from bson import ObjectId

class ProjectRepository:
    def __init__(self, db):
        self.collection = db.get_collection("project")

    async def find_projects_by_user(self, user_id: str):
        projects = self.collection.find({
            "$or": [
                {"owner": user_id},
                {"members.user_id": user_id}
            ]
        })
        return await projects.to_list()

    async def create(self, project_data: dict):
        result = await self.collection.insert_one(project_data)
        return str(result.inserted_id)
    
    async def find_by_id(self, project_id: str):
        project = await self.collection.find_one({"_id": ObjectId(project_id)})
        return project
    
    async def update_by_id(self, project_id: str, update_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": update_data}
        )
        return result
    async def delete_by_id(self, project_id: str):
        result = self.collection.delete_one({"_id": ObjectId(project_id)})
        return result
    
    async def update_members_by_id(self, project_id: str, members: dict):
        result = self.collection.update_one({"_id": ObjectId(project_id)}, {"$push": {"members": {"$each": members }}})
        return result