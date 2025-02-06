from pydantic import BaseModel
from datetime import datetime

class NotificationResponse(BaseModel):
    id: str 
    user_id: str
    message: str
    type: str
    status: str
    created_at: str