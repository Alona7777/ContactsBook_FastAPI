from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session

from src.database.db import get_db

from src.schemas.contacts import ContactBase, ContactResponse
from src.repository import  one_contact


router = APIRouter(prefix='/contact', tags=['contact'])


@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await one_contact.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

# @router.get('/{contact_email}', response_model=ContactResponse)
@router.get("/search", response_model=ContactResponse)
async def read_contact_by_email(contact_email: str = Path(..., title='Contact Email', description='Email of the contact'), db: Session = Depends(get_db)):
    contact = await one_contact.get_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.post('/', response_model=ContactResponse)
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    return await one_contact.create_contact(body, db)

@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    contact = await one_contact.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.delete('/{contact_id}', response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await one_contact.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact