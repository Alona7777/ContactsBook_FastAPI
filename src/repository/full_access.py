from typing import List, Type

from datetime import date, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas.contacts import ContactBase, ContactResponse


async def get_all_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    """
    The get_all_contacts function returns a list of all contacts in the database.
    
    :param skip: int: Skip a number of records in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass in the database session to be used
    :return: A list of contact objects
    :doc-author: Trelent
    """
    return db.query(Contact).offset(skip).limit(limit).all()

