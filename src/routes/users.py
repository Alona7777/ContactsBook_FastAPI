import cloudinary
import cloudinary.uploader
import pickle

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.schemas.user import UserBase, UserResponse, TokenBase, RequestEmail
from src.repository import  users as repositories_users
from src.services.auth import auth_service
from src.conf.config import config


router = APIRouter(prefix='/users', tags=['users'])

cloudinary.config(
    cloud_name=config.CLOUDINARY_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True,
)

@router.get('/me', response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)) -> User:
    """
    The get_current_user function is a dependency that will be injected into the
        get_current_user endpoint. It uses the auth_service to retrieve a user from
        the database, and if it finds one, returns it. If not, raises an HTTPException.
    
    :param user: User: Define the type of the parameter
    :return: The user object, which is passed to the
    :doc-author: Trelent
    """
    return user

@router.patch('/avatar', response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def update_avatar_user(file: UploadFile = File(), user: User = Depends(auth_service.get_current_user), 
                             db: Session = Depends(get_db)) -> User:
    """
    The update_avatar_user function takes a file and user as input,
        uploads the file to Cloudinary, updates the avatar_url of the user in
        our database with that of the uploaded image's URL, and returns an updated User object.
    
    :param file: UploadFile: Get the file from the request
    :param user: User: Get the current user
    :param db: Session: Get the database session
    :return: The updated user object
    :doc-author: Trelent
    """
    public_id = f'Web/{user.email}'
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop='fill', version=res.get('version')
    )
    user = await repositories_users.update_avatar_url(user.email, res_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user