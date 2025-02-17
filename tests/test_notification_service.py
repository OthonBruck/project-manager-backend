import pytest
from unittest.mock import AsyncMock, patch
from services.notification_service import NotificationService
from schemas.project import ProjectCreate, ProjectAddMember, ProjectDictAddMember
from utils.functions import serialize_document, serialize_list
from bson import ObjectId
from fastapi import HTTPException
from typing import List
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_notification_success():
    mock_repository = AsyncMock()
    date = datetime.now(timezone.utc)
    mock_repository.create.return_value =  {
        "user_id": "user_id",
        "message": "message",
        "type": "type_",
        "status": "unread",
        "created_at": date,
    }

    service = NotificationService(mock_repository)

    result = await service.create_notification("user_id", "message", "type_")

    assert result["user_id"] == "user_id"

    mock_repository.create.assert_called_once_with({
        "user_id": "user_id",
        "message": "message",
        "type": "type_",
        "status": "unread",
        "created_at": date,
    })

@pytest.mark.asyncio
async def test_get_notifications_success():
    mock_repository = AsyncMock()
    date = datetime.now(timezone.utc)
    mock_repository.find_notifications_by_user.return_value =  [{
        "user_id": "user_id",
        "message": "message",
        "type": "type_",
        "status": "unread",
        "created_at": date,
    }]

    service = NotificationService(mock_repository)

    result = await service.get_notifications("user_id")

    assert result[0]["user_id"] == 'user_id'
    mock_repository.find_notifications_by_user.assert_called_once_with("user_id")

@pytest.mark.asyncio
async def test_mark_as_read_success():
    mock_repository = AsyncMock()

    service = NotificationService(mock_repository)

    result = await service.mark_as_read("notification_id")

    mock_repository.update_by_id.assert_called_once_with({'_id': 'notification_id'}, {'$set': {'status': 'read'}})