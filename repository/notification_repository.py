from bson import ObjectId

class NotificationRepository:
    def __init__(self, db):
        self.collection = db.get_collection("notification")

    async def find_notifications_by_user(self, user_id: str):
        notifications = self.collection.find(
            {"user_id": user_id}
        )
        return await notifications.to_list()

    async def create(self, notification_data: dict):
        result = await self.collection.insert_one(notification_data)
        return str(result.inserted_id)
    
    async def update_mark_as_read_by_id(self, notification_id: str):
        result = self.collection.update_one(
            {"_id": notification_id},
            {"$set": {"status": "read"}}
        )
        return result
#TODO: Finish delete notifications
    async def delete_by_id(self, notification_id: str):
        result = self.collection.delete_one({"_id": ObjectId(notification_id)})
        return result