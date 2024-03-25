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

@router.get('/birthday_for_week', response_model=List[ContactResponse])
async def read_contacts_with_birth(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays_contacts(db)
    return contacts


@router.get("/search/{query}", response_model=list[ContactResponse])
async def search_contacts(query: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(query, db)
    return contacts


