from schemas.user import UserCreate, UserLogin
from utils.security import get_password_hash, verify_password
from fastapi import HTTPException
from bson.objectid import ObjectId
from utils.functions import serialize_document
from decouple import config
from datetime import datetime, timedelta, timezone
from jose import jwt

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Gera um token JWT"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config("SECRET_KEY"), algorithm=config("ALGORITHM"))

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
        if not result:
            raise HTTPException(status_code=400, detail="User does not exist.")
        return serialize_document(result)
    
    async def authenticate_user(userLogin: UserLogin, db):
        user = await db.get_collection("user").find_one({"email": userLogin.email})
        if not user or not verify_password(userLogin.password, user.get("hashed_password")):
            raise HTTPException(status_code=401, detail="Invalid credentials.")
        
        token = create_access_token({"sub": user.get("email")})
        return {'token': token}
    
