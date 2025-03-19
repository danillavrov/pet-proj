from authx import AuthXConfig, AuthX
import requests
from fastapi import FastAPI, Request, HTTPException, Depends

app = FastAPI()

AUTH_SERVICE_URL="http://0.0.0.0:8008/verify"
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)


def verify_jwt_from_cookie(request: Request):
    token = request.cookies.get("my_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    response = requests.post(AUTH_SERVICE_URL, json={"token": token})
    if response.status_code == 200:
        return response.json()["user"]

    raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/protected", dependencies=[Depends(verify_jwt_from_cookie)])
def protected_example():
    return {"data": "data"}
