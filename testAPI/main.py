import jwt
from authx import AuthXConfig, AuthX

from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from jwt import PyJWTError
from proj_pack import verify_jwt_from_header
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ALGORITHM = "HS256"
SECRET_KEY = 'super_secret_key'

@app.get("/protected")
async def protected_route(user_data: dict = Depends(verify_jwt_from_header)):
    return {"message": "Access granted", "user": user_data}
