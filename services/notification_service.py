from datetime import datetime, timedelta, timezone
from pymongo.collection import Collection
from utils.functions import serialize_list

class NotificationService:
    def __init__(self, db):
        self.db = db.get_collection('notification')

    async def create_notification(self, user_id: str, message: str, type_: str):
        notification = {
            "user_id": user_id,
            "message": message,
            "type": type_,
            "status": "unread",
            "created_at": datetime.now(timezone.utc),
        }
        await self.db.insert_one(notification)
        return notification

    async def get_notifications(self, user_id: str):
        notifications = await self.db.find({"user_id": user_id}).to_list()
        return serialize_list(notifications)

    async def mark_as_read(self, notification_id: str):
        await self.db.update_one(
            {"_id": notification_id},
            {"$set": {"status": "read"}}
        )
