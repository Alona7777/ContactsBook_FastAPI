from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas.contacts import ContactBase, ContactResponse

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function is used to retrieve a contact from the database.
    It takes in an integer representing the id of the contact, a user object, and a database session.
    The function returns either None or an instance of Contact.
    
    :param contact_id: int: Get the contact from the database
    :param user: User: Get the user from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

async def get_contact_by_email(contact_email: str, user: User, db: Session) -> Contact:
    """
    The get_contact_by_email function takes in a contact_email and user, and returns the first Contact object
        that matches the given email address.
    
    :param contact_email: str: Specify the email of the contact that we want to retrieve
    :param user: User: Get the user_id from the user object
    :param db: Session: Access the database
    :return: A contact object that matches the email address and user id
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.email == contact_email, Contact.user_id == user.id)).first()

async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
    
    :param body: ContactBase: Get the data from the request body
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: The newly created contact
    :doc-author: Trelent
    """
    contact = Contact(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        phone = body.phone,
        birth_date = body.birth_date,
        info = body.info,
        user_id = user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactBase): The updated information for the Contact object. 
    
    :param contact_id: int: Identify the contact that we want to delete
    :param body: ContactBase: Get the data from the request body
    :param user: User: Ensure that the user is authenticated and only updates their own contacts
    :param db: Session: Access the database
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.phone = body.phone,
        contact.birth_date = body.birth_date,
        contact.info = body.info 
        db.commit()
    return contact


async def update_name(contact_id: int, first_name: str, user: User, db: Session) -> Contact | None:
    """
    The update_name function updates the first name of a contact.
        Args:
            contact_id (int): The id of the contact to update.
            first_name (str): The new value for the contacts's first name.
    
    :param contact_id: int: Specify the contact to update
    :param first_name: str: Update the first name of a contact
    :param user: User: Get the user_id from the user object,
    :param db: Session: Access the database
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = first_name,
        db.commit()
    return contact

async def update_last_name(contact_id: int, last_name: str, user: User, db: Session) -> Contact | None:
    """
    The update_last_name function updates the last name of a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            last_name (str): The new value for the contacts's last name.
            user (User): A User object representing who is making this request.  This is used to ensure that only a user with permission can make this change, and that they cannot modify another users data by accident or on purpose!
    
    :param contact_id: int: Identify the contact to be updated
    :param last_name: str: Pass the new last name to be updated
    :param user: User: Ensure that the user is logged in and has access to the contact
    :param db: Session: Access the database
    :return: The updated contact, or none if the contact does not exist
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.last_name = last_name,
        db.commit()
    return contact

async def update_email(contact_id: int, email: str, user: User, db: Session) -> Contact | None:
    """
    The update_email function updates the email of a contact.
        Args:
            contact_id (int): The id of the contact to update.
            email (str): The new email for this user's contact.
    
    :param contact_id: int: Identify the contact to be updated
    :param email: str: Pass in the new email address
    :param user: User: Ensure that the user is authorized to update the contact
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.email = email,
        db.commit()
    return contact

async def update_phone(contact_id: int, phone: str, user: User, db: Session) -> Contact | None:
    """
    The update_phone function updates the phone number of a contact.
        Args:
            contact_id (int): The id of the contact to update.
            phone (str): The new phone number for this user's contact.
    
    :param contact_id: int: Identify the contact to be updated
    :param phone: str: Pass the new phone number to the function
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The updated contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.phone = phone,
        db.commit()
    return contact

async def update_info(contact_id: int, info: str, user: User, db: Session) -> Contact | None:
    """
    The update_info function updates the info field of a contact.
        Args:
            contact_id (int): The id of the contact to update.
            info (str): The new value for the info field.
    
    :param contact_id: int: Identify the contact to update
    :param info: str: Update the info field in the contact table
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A contact object or none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.info = info,
        db.commit()
    return contact

async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used for security purposes, so that users can only remove their own contacts and not other users' contacts. 
            db (Session): A session object which allows us to interact with our database in order to delete a row from it containing information about this particular Contact object we are deleting.
    
    :param contact_id: int: Specify which contact to delete
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact