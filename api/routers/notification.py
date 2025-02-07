from fastapi import APIRouter, Depends
from services.notification_service import NotificationService
from utils.functions import get_service
from schemas.api_response import ApiResponse
from schemas.notification import NotificationResponse
from bson import ObjectId
from typing import List

router = APIRouter()

# @router.post("/notifications/", response_model=NotificationResponse)
# async def create_notification(notification: NotificationCreate, service=Depends(get_service(NotificationService))):
#     service = NotificationService(db.notifications)
#     return await service.create_notification(notification.user_id, notification.message, notification.type)

@router.get("/{user_id}", response_model=ApiResponse[List[NotificationResponse]])
async def get_notifications(user_id: str, service=Depends(get_service(NotificationService))):
    notifications = await service.get_notifications(user_id)
    return {"message": "Notificações encontradas com sucesso", "data": notifications}

@router.patch("/{notification_id}/read")
async def mark_as_read(notification_id: str, service=Depends(get_service(NotificationService))):
    await service.mark_as_read(ObjectId(notification_id))
    return {"message": "Notificação marcada como lida"}
