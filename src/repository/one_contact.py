from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas.contacts import ContactBase, ContactResponse

async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def get_contact_by_email(contact_email: str, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.email == contact_email).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        phone = body.phone,
        birth_date = body.birth_date,
        info = body.info 
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.phone = body.phone,
        contact.birth_date = body.birth_date,
        contact.info = body.info 
        db.commit()
    return contact


async def update_name(contact_id: int, first_name: str, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = first_name,
        db.commit()
    return contact

async def update_last_name(contact_id: int, last_name: str, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.last_name = last_name,
        db.commit()
    return contact

async def update_email(contact_id: int, email: str, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.email = email,
        db.commit()
    return contact

async def update_phone(contact_id: int, phone: str, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.phone = phone,
        db.commit()
    return contact

async def update_info(contact_id: int, info: str, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.info = info,
        db.commit()
    return contact

async def remove_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact