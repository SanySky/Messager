from fastapi import Depends, APIRouter
from models import Message, User
from faststream.rabbit.fastapi import RabbitRouter


router = RabbitRouter("amqp://guest:guest@localhost:5672/")


@router.post('/message')
async def send_message(message: Message, user: User = Depends()):
    """Функция отправляет сообщение в RabbitMQ"""
    await router.publish(
        "messages", {
            "room_id": message.room_id,
            "content": message.content,
            "user": user.username
        }
    )
