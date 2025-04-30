from typing import AsyncGenerator

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


Base = declarative_base()


class user_stat(Base, AsyncAttrs):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_completed = Column(Integer, index=True)
    task_failed = Column(Integer, index=True)
    task_processed = Column(Integer, index=True)
