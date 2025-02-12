from datetime import datetime, timedelta, timezone
from pymongo.collection import Collection
from utils.functions import serialize_list

class NotificationService:
    def __init__(self, db):
        self.db = db

    async def create_notification(self, user_id: str, message: str, type_: str):
        collection = await self.db.get_collection('notification')
        notification = {
            "user_id": user_id,
            "message": message,
            "type": type_,
            "status": "unread",
            "created_at": datetime.now(timezone.utc),
        }
        await collection.insert_one(notification)
        return notification

    async def get_notifications(self, user_id: str):
        collection = await self.db.get_collection('notification')
        notifications = await collection.find({"user_id": user_id}).to_list()
        return serialize_list(notifications)

    async def mark_as_read(self, notification_id: str):
        collection = await self.db.get_collection('notification')
        await collection.update_one(
            {"_id": notification_id},
            {"$set": {"status": "read"}}
        )
