from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.auth.security import hash_password


# Створення нового користувача, якщо email ще не зареєстровано
def create_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return None  # Користувач з таким email вже існує
    new_user = User(email=user.email, username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Аутентифікація користувача за email та паролем
def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None  # Користувача з таким email не знайдено
    from app.auth.security import verify_password
    if not verify_password(password, user.hashed_password):
        return None  # Невірний пароль
    return user  # Успішна аутентифікація


# Функція для підтвердження email користувача
def update_user_email_confirmation(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.confirmed = True
        db.commit()
        db.refresh(user)
        return user
    return None


# Функція для оновлення аватара користувача
def update_user_avatar(db: Session, user: User, avatar_url: str):
    user_db = db.query(User).filter(User.id == user.id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_db.avatar = avatar_url
    db.commit()
    db.refresh(user_db)
    return user_db