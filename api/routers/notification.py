from fastapi import APIRouter, Depends
from services.notification_service import NotificationService
from schemas.api_response import ApiResponse
from schemas.notification import NotificationResponse
from bson import ObjectId
from typing import List
from db.database import get_database
from repository.notification_repository import NotificationRepository

router = APIRouter()

def get_service(db = Depends(get_database)):
    repository = NotificationRepository(db)
    return NotificationService(repository)

@router.get("/{user_id}", response_model=ApiResponse[List[NotificationResponse]])
async def get_notifications(user_id: str, service=Depends(get_service)):
    notifications = await service.get_notifications(user_id)
    return {"message": "Notificações encontradas com sucesso", "data": notifications}

@router.patch("/{notification_id}/read")
async def mark_as_read(notification_id: str, service=Depends(get_service)):
    await service.mark_as_read(ObjectId(notification_id))
    return {"message": "Notificação marcada como lida"}
