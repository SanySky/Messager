from fastapi import FastAPI, Depends, HTTPException
from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from models import Message, User

router = RabbitRouter("amqp://guest:guest@localhost:5672/")

app = FastAPI()
broker = router.broker


async def connect_broker():
    try:
        await broker.connect()
    except Exception as e:
        print(f"Ошибка при подключении к брокеру: {e}")


async def create_queue():
    try:
        await broker.declare_queue(RabbitQueue("message"))
    except Exception as e:
        print(f"Ошибка при создании очереди: {e}")


@app.on_event("startup")
async def startup_event():
    await connect_broker()
    await create_queue()


@app.post('/message')
async def send_message(message: Message, user: User = Depends()):
    """Функция отправляет сообщение в RabbitMQ"""
    try:
        await broker.publish(
            queue="message",
            message={
                "room_id": message.room_id,
                "content": message.content,
                "user": user.username
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при отправке сообщения: {e}")

app.include_router(router)
