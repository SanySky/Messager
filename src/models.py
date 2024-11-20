from pydantic import BaseModel


class Message(BaseModel):
    """Модель сообщения"""
    room_id: str
    content: str


class User(BaseModel):
    """Модель пользователя"""
    username: str
