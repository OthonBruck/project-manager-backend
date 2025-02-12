from fastapi import APIRouter, Depends, status
from schemas.user import UserCreate, UserResponseCreate, UserResponseGet, UserLogin, UserResponseLogin
from schemas.api_response import ApiResponse
from services.user_service import UserService
from utils.security import get_current_user
from utils.functions import get_database
from repository.user_repository import UserRepository

router = APIRouter()

def get_service(db = Depends(get_database)):
    repository = UserRepository(db)
    return UserService(repository)

@router.post("/", response_model=ApiResponse[UserResponseCreate], status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, service=Depends(get_service)):
    user_response = await service.create_user(user)
    return {"message": "Usuário criado com sucesso", "data": user_response}

@router.get("/{id}", response_model=ApiResponse[UserResponseGet], status_code=status.HTTP_200_OK)
async def get_user(id, service=Depends(get_service), current_user=Depends(get_current_user)):
    user_response = await service.get_user_by_id(id)
    return {"message": "Usuário encontrado com sucesso", "data": user_response}

@router.post("/login", response_model=ApiResponse[UserResponseLogin], status_code=status.HTTP_200_OK)
async def login(user: UserLogin, service=Depends(get_service)):
    token = await service.authenticate_user(user)
    return {"message": "Usuário autenticado com sucesso", "data": token}
