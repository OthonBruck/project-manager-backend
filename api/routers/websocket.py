from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from services.websocket_service import connect_user, disconnect_user

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await connect_user(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await disconnect_user(user_id)
