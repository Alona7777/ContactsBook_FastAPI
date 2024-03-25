from typing import List

from datetime import date, timedelta
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas.contacts import ContactBase, ContactResponse


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contacts_by_name(contact_name: str, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.first_name == contact_name).first()

async def get_contacts_by_last_name(contact_last_name: str, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.last_name == contact_last_name).all()


async def get_upcoming_birthdays_contacts(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        and_(
            Contact.birth_date >= today,
            Contact.birth_date <= end_date
        )
    ).all()
    return contacts



