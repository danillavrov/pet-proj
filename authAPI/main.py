import jwt
from fastapi import FastAPI, HTTPException, Depends, Request, Response, requests, Header
from authx import AuthX, AuthXConfig
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models import get_async_session, User
from schemas import UserSchema
from proj_pack import verify_jwt_from_header
from sqlalchemy.future import select

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/reg")
async def register(user: UserSchema, db: AsyncSession = Depends(get_async_session)):
    new_user = User(name=user.name, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User registered successfully"}


@app.post("/login")
async def login(creds: UserSchema, db: AsyncSession = Depends(get_async_session)):
    query = await db.execute(select(User).where(User.name == creds.name))
    user = query.scalar_one_or_none()
    data = {"username": creds.name, "id": user.id}
    to_encode = data.copy()
    if not user:
        raise HTTPException(detail="User not found", status_code=401)
    if creds.password == user.password:
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "message": "success"}
    raise HTTPException(status_code=401, detail="Incorrect password")


@app.get("/protected")
async def protected_route(user_data: dict = Depends(verify_jwt_from_header)):
    return {"message": "Access granted", "user": user_data}
