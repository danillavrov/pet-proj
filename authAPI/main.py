from fastapi import FastAPI, HTTPException, Depends
from authx import AuthX, AuthXConfig
from fastapi import Response
from sqlalchemy.orm import Session

from models import SessionLocal, User
from schemas import UserSchema

app = FastAPI()


config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/reg")
def register(user: UserSchema, db: Session = Depends(get_db)):
    new_user = User(name=user.name, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(creds: UserSchema, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(name=creds.name).first()
    if not user:
        raise HTTPException(detail="User not found", status_code=401)
    if creds.password == user.password:
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect password")


@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected_example():
    return {"data": "data"}

