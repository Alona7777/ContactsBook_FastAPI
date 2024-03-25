from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session

from src.database.db import get_db

from src.schemas.contacts import ContactBase, ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts

@router.get('/{contact_name}', response_model=ContactResponse)
async def read_contacts_by_name(contact_name: str = Path(..., title="Contact Name", description="Name of the contact"), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contacts_by_name(contact_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.get('/{contact_last_name}',response_model=List[ContactResponse])
async def read_contacts_by_last_name(contact_last_name: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contacts_by_last_name(contact_last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.get('/birthday_for_week', response_model=List[ContactResponse])
async def read_contacts_with_birth(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays_contacts(db)
    return contacts




