import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from proj_pack import verify_jwt_from_header
from fastapi import FastAPI, Depends, Request
from models import Task, get_async_session
from schemas import TaskSchema
from contextlib import asynccontextmanager
import aio_pika

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
QUEUE_NAME = "user_events"

@asynccontextmanager
async def lifespan(app: FastAPI):

    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.declare_queue(QUEUE_NAME, durable=True)


    app.state.rabbit_connection = connection
    app.state.rabbit_channel = channel

    yield

    await connection.close()

app = FastAPI(lifespan=lifespan)

AUTH_SERVICE_URL = "http://0.0.0.0:8008/verify"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add_task")
async def add_task(task: TaskSchema, db: AsyncSession = Depends(get_async_session),
                   user_data: dict = Depends(verify_jwt_from_header)):
    user_id = user_data.get("id")
    new_task = Task(user=user_id, title=task.title, description=task.description)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return {"message": "success"}

@app.get("/get_task")
async def get_tasks(db: AsyncSession = Depends(get_async_session), user_data: dict = Depends(verify_jwt_from_header)):
    user_id = user_data.get("id")
    query = await db.execute(select(Task).where(Task.user == user_id))
    res = query.scalars().all()
    return res

@app.post("/task_management")
async def set_task_status(task_status: str, request: Request):
    user_id = 1
    channel: aio_pika.Channel = request.app.state.rabbit_channel
    payload = {'task_status': task_status, 'user': user_id}
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key=QUEUE_NAME
    )



















