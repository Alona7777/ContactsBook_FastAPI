from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role, Contact

from src.services.auth import auth_service
from src.services.roles import RoleAccess

from src.schemas.contacts import ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)) -> List[Contact]:
    """
    The read_contacts function returns a list of contacts.
    
    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A list of contacts, which is the same type as the contact class
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get('/birthday_for_week', response_model=List[ContactResponse])
async def read_contacts_with_birth(db: Session = Depends(get_db), 
                                   current_user: User = Depends(auth_service.get_current_user)) -> List[Contact]:
    """
    The read_contacts_with_birth function returns a list of contacts with upcoming birthdays.
        The function takes in the current user and database session as parameters, and uses them to get the list of contacts from the repository_contacts module.
    
    
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user, and the db: session parameter is used to get a database session
    :return: A list of contacts with upcoming birthdays
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_upcoming_birthdays_contacts(current_user, db)
    return contacts


@router.get('/search/{query}', response_model=list[ContactResponse])
async def search_contacts(query: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)) -> List[Contact]:
    """
    The search_contacts function searches for contacts in the database.
        It takes a query string as an argument and returns a list of contacts that match the query.
    
    :param query: str: Search for contacts in the database
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(query, current_user, db)
    return contacts


