import jwt
from fastapi import Header, HTTPException
from jwt import PyJWTError


def verify_jwt_from_header(authorization: str = Header(...), SECRET_KEY: str = "super_secret_key", ALGORITHM='HS256'):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Можно вернуть полезные данные, например user_id
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")