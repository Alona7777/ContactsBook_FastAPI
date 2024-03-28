from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.schemas.contacts import ContactBase, ContactResponse
from src.repository import  one_contact

from src.services.auth import auth_service


router = APIRouter(prefix='/contact', tags=['contact'])


@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.get('/search/{email}', response_model=ContactResponse)
async def read_contact_by_email(email: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.get_contact_by_email(email, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await one_contact.create_contact(body, current_user, db)

@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.patch('/update_name/{contact_id}/{first_name}', response_model=ContactResponse)
async def update_name(contact_id: int, first_name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.update_name(contact_id, first_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.patch('/update_last_name/{contact_id}/{last_name}', response_model=ContactResponse)
async def update_last_name(contact_id: int, last_name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.update_last_name(contact_id, last_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.patch('/update_email/{contact_id}/{email}', response_model=ContactResponse)
async def update_email(contact_id: int, email: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.update_email(contact_id, email, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.patch('/update_phone/{contact_id}/{phone}', response_model=ContactResponse)
async def update_phone(contact_id: int, phone: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.update_phone(contact_id, phone, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.patch('/update_info/{contact_id}/{info}', response_model=ContactResponse)
async def update_phone(contact_id: int, info: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.update_info(contact_id, info, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.delete('/{contact_id}', response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await one_contact.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact