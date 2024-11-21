from fastapi import Depends, WebSocket, WebSocketDisconnect
from faststream.rabbit.fastapi import RabbitRouter
from models import User
from main import router

connected_users = {}


@router.websocket('/updates/{room_id}')
async def get_updates(websocket: WebSocket, room_id: str, user: User = Depends()):
    """Вебсокет для получения сообщений"""
    await websocket.accept()

    if room_id not in connected_users:
        connected_users[room_id] = []


    if len(connected_users[room_id]) >= 2:
        await websocket.close()
        return

    connected_users[room_id].append(websocket)

    try:
        while True:
            message = await router.consume("message")
            if message['room_id'] == room_id:
                for conn in connected_users[room_id]:
                    await conn.send_json({"user": message['user'], "content": message['content']})
    except WebSocketDisconnect:
        connected_users[room_id].remove(websocket)
        if not connected_users[room_id]:
            del connected_users[room_id]
