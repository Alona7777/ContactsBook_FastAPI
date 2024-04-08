from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.schemas.user import UserBase, UserResponse, TokenBase, RequestEmail
from src.repository import  users as repository_users
from src.services.auth import auth_service



router = APIRouter(prefix='/users', tags=['users'])

@router.get('/me', response_model=UserResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user
