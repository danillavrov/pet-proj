from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from proj_pack import verify_jwt_from_header
from fastapi import FastAPI, Depends
from models import Task, get_async_session

from schemas import TaskSchema

app = FastAPI()
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
