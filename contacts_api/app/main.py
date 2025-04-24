from . import models
from .database import engine
from .routes import contacts
from fastapi import FastAPI
from app.routes import auth
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import cloudinary

load_dotenv()

cloudinary.config(
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key = os.getenv("CLOUDINARY_API_KEY"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET")
)

# Створення всіх таблиць у базі даних на основі моделей
models.Base.metadata.create_all(bind=engine)

# Ініціалізація FastAPI-додатку
app = FastAPI()

origins = [
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Головний маршрут (корінь) — повертає привітальне повідомлення
@app.get("/")
def read_root():
    return {"message": "Welcome to the contacts API, my homework!"}


# Підключення мaршруту для контактів (CRUD та додаткові функції)
app.include_router(contacts.router)
app.include_router(auth.router)

# Ініціалізація підключення до Redis
@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_client)

# Закриття підключення до Redis
@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()
