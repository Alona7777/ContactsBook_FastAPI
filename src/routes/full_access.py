from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role, Contact

from src.services.auth import auth_service
from src.services.roles import RoleAccess

from src.schemas.contacts import ContactBase, ContactResponse, ContactResponseAdmin
from src.repository import full_access


router = APIRouter(prefix='/all', tags=['all'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


@router.get('/', response_model=List[ContactResponseAdmin], dependencies=[Depends(access_to_route_all)])
async def get_all_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[Contact]:
    """
    The get_all_contacts function returns a list of all contacts in the database.
        The skip and limit parameters are used to paginate the results, with skip being how many records to skip before returning results, and limit being how many records to return after skipping.
        If no values are provided for these parameters, they default to 0 and 100 respectively.
    
    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await full_access.get_all_contacts(skip, limit, db)
    return contacts