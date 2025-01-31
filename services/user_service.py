from schemas.user import UserCreate
from utils.security import get_password_hash
from fastapi import HTTPException

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate, db):

        hashed_password = get_password_hash(user_data.password)
        new_user = {
            "name": user_data.name,
            "email": user_data.email,
            "hashed_password": hashed_password,
        }

        existing_user = await db["users"].find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already in use.")

        result = await db["users"].insert_one(new_user)
        new_user["name"] = result.inserted_id 
        return new_user
