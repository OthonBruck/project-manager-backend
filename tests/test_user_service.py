import pytest
from unittest.mock import AsyncMock, patch
from services.user_service import UserService
from schemas.user import UserCreate, UserLogin
from utils.functions import serialize_document, serialize_list
from bson import ObjectId
from fastapi import HTTPException
from typing import List
from datetime import datetime, timezone

@pytest.mark.asyncio
@patch("services.user_service.get_password_hash")
async def test_create_task_success(mock_check_permission):
    mock_check_permission.return_value = "hashed_password"
    mock_repository = AsyncMock()

    mock_repository.create.return_value =  {
        "email":"teste@gmail.com",
        "name":"login",
        "password": "hashed_password",
    }

    mock_repository.find_by_email.return_value = False

    service = UserService(mock_repository)

    user_data = UserCreate(email="teste@gmail.com", name="login", password="password")

    result = await service.create_user(user_data)

    assert result["hashed_password"] == "hashed_password"

@pytest.mark.asyncio
async def test_get_user_by_id_success():
    fake_user_id = str(ObjectId())

    mock_repository = AsyncMock()

    fake_user =  {
        "_id": fake_user_id,
        "email":"teste@gmail.com",
        "name":"login",
        "password": "hashed_password"
    }

    mock_repository.find_user_by_id.return_value = fake_user

    service = UserService(mock_repository)
    result = await service.get_user_by_id(fake_user_id)

    assert result == serialize_document(fake_user)

    mock_repository.find_user_by_id.assert_called_once_with(fake_user_id)

@pytest.mark.asyncio
@patch("services.user_service.create_access_token")
@patch("services.user_service.verify_password")
async def test_authenticate_user_success(mock_verify_password, mock_create_access_token):
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "token"

    fake_user_id = str(ObjectId())

    mock_repository = AsyncMock()

    fake_user =  {
        "_id": fake_user_id,
        "email":"teste@gmail.com",
        "name":"login",
        "password": "hashed_password"
    }

    mock_repository.find_by_email.return_value = fake_user

    userLogin = UserLogin(email= "teste@gmail.com", password =  "hashed_password")

    service = UserService(mock_repository)
    result = await service.authenticate_user(userLogin)

    assert result == {"token": "token"}
