from datetime import datetime, timedelta, timezone
from pymongo.collection import Collection
from utils.functions import serialize_list
from repository.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    async def create_notification(self, user_id: str, message: str, type_: str):
        notification = {
            "user_id": user_id,
            "message": message,
            "type": type_,
            "status": "unread",
            "created_at": datetime.now(timezone.utc),
        }
        await self.repository.create(notification)
        return notification

    async def get_notifications(self, user_id: str):
        notifications = await self.repository.find_notifications_by_user(user_id)
        return serialize_list(notifications)

    async def mark_as_read(self, notification_id: str):
        await self.repository.update_by_id(
            {"_id": notification_id},
            {"$set": {"status": "read"}}
        )
