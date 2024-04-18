from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.schemas.user import UserBase, UserResponse, TokenBase, RequestEmail
from src.repository import  users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email


router = APIRouter(prefix='/auth', tags=['auth'])

get_refresh_token = HTTPBearer()

@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserBase, bt: BackgroundTasks, request: Request, db: Session = Depends(get_db)) -> User:
    """
    The signup function creates a new user in the database.
        It takes a UserBase object as input, which contains the following fields:
            - email (required): The email address of the user to be created. Must be unique.
            - password (required): The password for this account, hashed using Argon2 by default.
    
    :param body: UserBase: Get the user's email and password from the request body
    :param bt: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base_url of the request
    :param db: Session: Get a database session
    :return: A userbase object, which is a subset of the full user model
    :doc-author: Trelent
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exists')
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post('/login', response_model=TokenBase)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    The login function is used to authenticate a user.
        It takes an email and password as input, and returns an access token if the credentials are valid.
    
    :param body: OAuth2PasswordRequestForm: Get the username and password from the body of a post request
    :param db: Session: Get a database session
    :return: A dict with the access_token, refresh_token and token type
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email')
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email not confirmed')
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password')
    access_token = await auth_service.create_access_token(data={'sub': user.email})
    refresh_token = await auth_service.create_refresh_token(data={'sub': user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@router.get('/refresh_token', response_model=TokenBase)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                         db: Session = Depends(get_db)):
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns an access token, 
        a new refresh token, and the type of authorization.
    
    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Access the database
    :return: An access_token and a refresh_token
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user: User = repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    
    access_token = await auth_service.create_access_token(data={'sub': email})
    refresh_token = await auth_service.create_refresh_token(data={'sub': email})
    await repository_users.update_token(user, refresh_token, db)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    The confirmed_email function takes a token and db as parameters.
        The token is the confirmation email's unique identifier, which is used to confirm the user's email address.
        The db parameter is a database session that will be used to query for users in our database.
    
    :param token: str: Get the token from the url
    :param db: Session: Get the database session
    :return: A dictionary with a message
    :doc-author: Trelent
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Verification error')
    if user.confirmed:
        return {'message': 'Your email is already confirmed'}
    await repository_users.confirmed_email(email, db)
    return {'massage': 'Email confirmed'}


@router.post('/request_email')
async def request_email(body: RequestEmail, bt: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    The request_email function is used to send an email to the user with a link
    to confirm their account. The function takes in a RequestEmail object, which
    contains the user's email address. It then checks if that email exists in our database, and if it does, sends an 
    email containing a confirmation link.
    
    :param body: RequestEmail: Get the email from the request body
    :param bt: BackgroundTasks: Add a task to the background tasks
    :param request: Request: Get the base url of the server
    :param db: Session: Get the database session
    :return: A message that will be displayed on the frontend
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {'message': 'Your email is already confirmed'}
    if user:
        bt.add_task(send_email, user.email, user.username, str(request.base_url))
    return {'message': 'Check your email for confirmation.'}
