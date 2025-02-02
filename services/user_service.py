from schemas.user import UserCreate
from utils.security import get_password_hash
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate, db):

        hashed_password = get_password_hash(user_data.password)
        new_user = {
            "name": user_data.name,
            "email": user_data.email,
            "hashed_password": hashed_password,
        }

        existing_user = await db.get_collection("user").find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already in use.")
        
        await db.get_collection("user").insert_one(new_user)

        return new_user
    
    async def get_user_by_id(id, db):
        result = await db.get_collection("user").find_one({"_id": ObjectId(id)})
        return serialize_document(result)