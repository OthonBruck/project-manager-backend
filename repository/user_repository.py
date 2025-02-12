from bson import ObjectId

class UserRepository:
    def __init__(self, db):
        self.collection = db.get_collection("user")

    async def find_user_by_id(self, user_id: str):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return await user

    async def create(self, project_data: dict):
        result = await self.collection.insert_one(project_data)
        return str(result.inserted_id)
    
    async def find_by_email(self, email: str):
        user = await self.collection.find_one({"email": email})
        return user
    
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