import jwt
from fastapi import FastAPI, HTTPException, Depends, Request, Response, requests
from authx import AuthX, AuthXConfig
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models import SessionLocal, User
from schemas import UserSchema

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)
ALGORITHM = "HS256"

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

        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            secure=True,
            samesite="none"  # Разрешает кросс-доменные куки
        )

        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect password")


def verify_jwt_from_cookie(request: Request):
    token = request.cookies.get("my_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    return {"data": "data"}

@app.get("/protected", dependencies=[Depends(verify_jwt_from_cookie)])
def protected_example():
    return {"data": "data"}


@app.post("/verify")
def verify_token(request: Request):
    token = request.json().get("token")
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "user": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

