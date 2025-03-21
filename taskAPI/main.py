

from authx import AuthXConfig, AuthX
import requests
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Task
from models import SessionLocal
from schemas import TaskSchema
app = FastAPI()
AUTH_SERVICE_URL="http://0.0.0.0:8008/verify"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_jwt_from_cookie(request: Request):
    token = request.cookies.get("my_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    response = requests.post(AUTH_SERVICE_URL, json={"token": token})
    if response.status_code == 200:
        return response.json()["user"]

    raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_user_from_jwt(request: Request):
    ...
@app.post("/add_task", dependencies=[Depends(verify_jwt_from_cookie)])
def add_task(task: TaskSchema, db: Session = Depends(get_db)):
    new_task = Task(user=task.name, name=task.name, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "success"}