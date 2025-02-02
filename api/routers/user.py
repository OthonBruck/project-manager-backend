from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserResponseCreate, UserResponseGet
from schemas.api_response import ApiResponse
from services.user_service import UserService
from db.database import get_database

router = APIRouter()

@router.post("/", response_model=ApiResponse[UserResponseCreate], status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db=Depends(get_database)):
    user_response = await UserService.create_user(user, db)
    return {"message": "Usuário criado com sucesso", "data": user_response}

@router.get("/{id}", response_model=ApiResponse[UserResponseGet], status_code=status.HTTP_200_OK)
async def get_user(id, db=Depends(get_database)):
    user_response = await UserService.get_user_by_id(id, db)
    return {"message": "Usuário encontrado com sucesso", "data": user_response}
