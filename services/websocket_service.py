from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

connected_users: Dict[str, WebSocket] = {}

async def connect_user(user_id: str, websocket: WebSocket):
    await websocket.accept()
    connected_users[user_id] = websocket

async def disconnect_user(user_id: str):
    connected_users.pop(user_id, None)

async def send_notification(message: dict, user_ids: list):
    for user_id in user_ids:
        if user_id in connected_users:
            await connected_users[user_id].send_json(message)
