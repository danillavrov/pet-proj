from fastapi import FastAPI
from contextlib import asynccontextmanager
import aio_pika
import asyncio
import json

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
QUEUE_NAME = "user_events"

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}