from authx import AuthXConfig, AuthX

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# AUTH_SERVICE_URL="http://0.0.0.0:8008/verify"
# config = AuthXConfig()
# config.JWT_SECRET_KEY = "SECRET_KEY"
# config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
# config.JWT_TOKEN_LOCATION = ["cookies"]
# security = AuthX(config=config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://0.0.0.0:8080"],  # Разрешённые источники (замени на свой фронтенд)
    allow_credentials=True,  # Разрешаем отправку куков
    allow_methods=["*"],  # Разрешаем все HTTP-методы (POST, GET, OPTIONS и т. д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)
# НЕ РАБОТАЕТ
# def verify_jwt_from_cookie(request: Request):
#     token = request.cookies.get("my_access_token")
#     if not token:
#         raise HTTPException(status_code=401, detail="Missing token")
#     response = requests.post(AUTH_SERVICE_URL, json={"token": token})
#     if response.status_code == 200:
#         return response.json()["user"]
#
#     raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/protected")
def protected_example(request: Request):
    print(request.cookies)
    token = request.cookies.get("my_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token =)")
    else:
        return {"data": "data"}
