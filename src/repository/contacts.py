from typing import List, Type

from datetime import date, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.
    
    :param skip: int: Skip a number of records in the database
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def search_contacts(query: str, user: User, db: Session) -> list[Type[Contact]]:
    """
    The search_contacts function takes in a query string and a user object,
    and returns all contacts that match the query. The search is case-insensitive.
    
    :param query: str: Search for contacts that match the query
    :param user: User: Get the user id of the user who is logged in
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
    ).all()
    return contacts


async def get_upcoming_birthdays_contacts(user: User, db: Session) -> List[Contact]:
    """
    The get_upcoming_birthdays_contacts function takes in a user and a database session,
    and returns all contacts that have birthdays within the next 7 days.
    
    
    :param user: User: Get the user id from the database
    :param db: Session: Connect to the database
    :return: A list of contacts whose birthdays are within the next 7 days
    :doc-author: Trelent
    """
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts: List[Contact] = db.query(Contact).filter(Contact.user_id == user.id).all()
    contacts_per_week = []
    for contact in contacts:
        if contact.birth_date:
            birth = contact.birth_date.replace(year=today.year)
            if birth < today - timedelta(days=1):
                birth = birth.replace(year=today.year+1)
            if today <= birth <= end_date:
                contacts_per_week.append(contact)
    return contacts_per_week



