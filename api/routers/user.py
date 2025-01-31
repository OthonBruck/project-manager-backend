from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserResponse
from services.user_service import create_user
from db.database import get_database

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    user_response = await create_user(user, db=Depends(get_database))
    return {"message": "Usuário criado com sucesso", "data": user_response}
