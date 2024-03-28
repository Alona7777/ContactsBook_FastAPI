from typing import List, Type

from datetime import date, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas.contacts import ContactBase, ContactResponse


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def search_contacts(query: str, user: User, db: Session) -> list[Type[Contact]]:
    contacts = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
    ).all()
    return contacts


async def get_upcoming_birthdays_contacts(user: User, db: Session) -> List[Contact]:
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    contacts_per_week = []
    for contact in contacts:
        birth = contact.birth_date.replace(year=today.year)
        if birth < today - timedelta(days=1):
            birth = birth.replace(year=today.year+1)
        if today <= birth <= end_date:
            contacts_per_week.append(contact)
    return contacts_per_week



