from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Contact, User
from app.schemas import ContactCreate


# Створення нового контакту, пов’язаного з поточним користувачем
def create_contact(db: Session, contact: ContactCreate, current_user: User):
    db_contact = Contact(**contact.dict(), user_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Отримання всіх контактів, які належать поточному користувачеві
def get_all_contacts(db: Session, current_user: User):
    return db.query(Contact).filter(Contact.user_id == current_user.id).all()


# Отримання одного контакту за ID, якщо він належить поточному користувачеві
def get_contact_by_id(contact_id: int, db: Session, current_user: User):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()


# Оновлення інформації про контакт, якщо він належить користувачеві
def update_contact(contact_id: int, contact: ContactCreate, db: Session, current_user: User):
    db_contact = get_contact_by_id(contact_id, db, current_user)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    return None


# Видалення контакту, якщо він належить користувачеві
def delete_contact(contact_id: int, db: Session, current_user: User):
    db_contact = get_contact_by_id(contact_id, db, current_user)
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None


# Пошук контактів користувача за ім’ям, прізвищем або email (частковий збіг)
def search_contacts(first_name: str = None, last_name: str = None, email: str = None, db: Session = None,
                    current_user: User = None):
    query = db.query(Contact).filter(Contact.user_id == current_user.id)

    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    return query.all()


# Отримання списку контактів з днями народження протягом наступних 7 днів
def get_upcoming_birthdays(db: Session, current_user: User):
    today = datetime.today().date()
    end_date = today + timedelta(days=7)

    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).all()
    upcoming = []

    for contact in contacts:
        bday = contact.birth_date.replace(year=today.year)
        if today <= bday <= end_date:
            upcoming.append(contact)

    return upcoming
