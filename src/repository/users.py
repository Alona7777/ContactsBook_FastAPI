from libgravatar import Gravatar

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.user import UserBase, UserResponse

async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it returns None.
    
    :param email: str: Specify the type of input that is expected
    :param db: Session: Pass the database session to the function
    :return: A user object, or none if the user does not exist
    :doc-author: Trelent
    """
    user = db.query(User).filter(User.email == email).first()
    return user

async def create_user(body: UserBase, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
    
    :param body: UserBase: Pass in the user data from the request body
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)
    user = User(**body.model_dump(), avatar=avatar)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

 
async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.
    
    :param user: User: Get the user's id
    :param token: str | None: Store the token in the database
    :param db: Session: Update the database with the new refresh token
    :return: Nothing
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()

    
async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes an email and a database session as arguments.
    It then gets the user by their email, sets their confirmed status to True, and commits the change.
    
    :param email: str: Get the email address of the user
    :param db: Session: Pass the database session to the function
    :return: None, but does not return a value
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar_url(email: str, url: str | None, db: Session) -> User:
    """
    The update_avatar_url function updates the avatar URL for a user.
    
    :param email: str: Get the user by email
    :param url: str | None: Specify that the url parameter can either be a string or none
    :param db: Session: Pass the database session into the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    db.refresh(user)
    return user

