from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# Схема для створення нового контакту (вхідні дані)
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None


# Схема відповіді при отриманні контакту (включає id)
class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True


# Схема для створення користувача (реєстрація)
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


# Схема відповіді для користувача
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# Схема токена для авторизації
class Token(BaseModel):
    access_token: str
    token_type: str
