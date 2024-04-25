from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Contact
from src.conf import messages

from src.schemas.contacts import ContactBase, ContactResponse
from src.repository import one_contact

from src.services.auth import auth_service


router = APIRouter(prefix="/contact", tags=["contact"])


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The read_contact function returns a contact by its id.
        If the contact does not exist, it raises an HTTP 404 error.


    :param contact_id: int: Specify the contact id to be read
    :param db: Session: Get the database session
    :param current_user: User: Get the user from the request
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await one_contact.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.get("/search/{email}", response_model=ContactResponse)
async def read_contact_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The read_contact_by_email function takes an email address and returns the contact associated with that email.
        If no such contact exists, it raises a 404 error.

    :param email: str: Specify the email of the contact that we want to retrieve
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await one_contact.get_contact_by_email(email, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        It takes a ContactBase object as input, and returns the newly created contact's ID.

    :param body: ContactBase: Get the data from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the user who is making the request
    :return: The contact that was created
    :doc-author: Trelent
    """
    return await one_contact.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactBase,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The update_contact function updates a contact in the database.
        It takes a ContactBase object, which is defined in schemas.py, and uses it to update an existing contact's information.

    :param body: ContactBase: Get the contact information from the request body
    :param contact_id: int: Identify the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user from the database
    :return: The contact that was updated
    :doc-author: Trelent
    """
    contact = await one_contact.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.patch("/update_name/{contact_id}/{first_name}", response_model=ContactResponse)
async def update_name(
    contact_id: int,
    first_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The update_name function updates the first name of a contact.
        The function takes in an integer, contact_id, which is used to find the correct contact.
        It also takes in a string, first_name, which will be used as the new value for that contacts' first name.

    :param contact_id: int: Specify the id of the contact to be updated
    :param first_name: str: Set the first name of the contact
    :param db: Session: Get a database session
    :param current_user: User: Get the user_id of the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await one_contact.update_name(contact_id, first_name, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.patch(
    "/update_last_name/{contact_id}/{last_name}", response_model=ContactResponse
)
async def update_last_name(
    contact_id: int,
    last_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The update_last_name function updates the last name of a contact.
        The function takes in an integer, contact_id, and a string, last_name.
        It returns the updated Contact object.

    :param contact_id: int: Specify the contact that is being updated
    :param last_name: str: Pass the last name of the contact to be updated
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: The contact with the updated last name
    :doc-author: Trelent
    """
    contact = await one_contact.update_last_name(
        contact_id, last_name, current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.patch("/update_email/{contact_id}/{email}", response_model=ContactResponse)
async def update_email(
    contact_id: int,
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The update_email function updates the email of a contact.
        The function takes in an integer, contact_id, and a string, email.
        It returns the updated Contact object.

    :param contact_id: int: Identify the contact to update
    :param email: str: Update the email of a contact
    :param db: Session: Get the database session
    :param current_user: User: Get the user_id of the current user
    :return: The updated contact object
    :doc-author: Trelent
    """
    contact = await one_contact.update_email(contact_id, email, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.patch("/update_phone/{contact_id}/{phone}", response_model=ContactResponse)
async def update_phone(
    contact_id: int,
    phone: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The update_phone function updates the phone number of a contact.
        Args:
            contact_id (int): The id of the contact to update.
            phone (str): The new phone number for this user's contacts.

    :param contact_id: int: Find the contact in the database
    :param phone: str: Get the phone number from the request body
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the auth_service module
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await one_contact.update_phone(contact_id, phone, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.patch("/update_info/{contact_id}/{info}", response_model=ContactResponse)
async def update_phone(
    contact_id: int,
    info: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The update_phone function takes a contact_id and an info string,
        and updates the phone number of the contact with that id.
        If no such contact exists, it raises a 404 error.

    :param contact_id: int: Specify the contact to update
    :param info: str: Update the phone number of a contact
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await one_contact.update_info(contact_id, info, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """
    The remove_contact function removes a contact from the database.
        It takes in an integer, contact_id, and returns a ContactResponse object.
        If the user is not logged in or if there is no such contact with that id, it raises an HTTPException.

    :param contact_id: int: Specify the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await one_contact.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_CONTACT
        )
    return contact
