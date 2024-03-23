from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, PhoneNumber, ContactPhone
from src.schemas.schema_contacts import ContactBase, ContactResponse, PhoneBase


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, body_phone:PhoneBase, db: Session) -> Contact:
    contact = Contact(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        birth_date = body.birth_date,
        info = body.info 
    )
    # contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    contact_id = db.query(Contact).filter(Contact.email == contact.email).first().id
    phone = PhoneNumber(phone=body_phone.phone)
    db.add(phone)
    db.commit()
    db.refresh(phone)
    phone_id = db.query(PhoneNumber).filter(PhoneNumber.phone == phone.phone)
    contact_phone = ContactPhone(
        contact_id=contact_id, 
        phone_id=phone_id)
    return contact, phone, contact_phone




async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.birth_date = body.birth_date,
        contact.info = body.info 
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
