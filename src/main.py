from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter
from routers import router


app = FastAPI()
app.include_router(router)
