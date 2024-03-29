from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role

from src.services.auth import auth_service
from src.services.roles import RoleAccess

from src.schemas.contacts import ContactBase, ContactResponse, ContactResponseAdmin
from src.repository import full_access


router = APIRouter(prefix='/all', tags=['all'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


@router.get('/', response_model=List[ContactResponseAdmin], dependencies=[Depends(access_to_route_all)])
async def get_all_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await full_access.get_all_contacts(skip, limit, db)
    return contacts