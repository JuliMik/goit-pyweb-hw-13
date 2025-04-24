# services/auth.py
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import EmailStr

# Налаштування для токену
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24


# Генерація токену для верифікації email
def create_email_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Витягування email з токену
def verify_email_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["sub"]
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=422, detail="Invalid token")
