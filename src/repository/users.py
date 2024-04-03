from typing import List, Type
from libgravatar import Gravatar

from datetime import date, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.user import UserBase, UserResponse

async def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user

async def create_user(body: UserBase, db: Session) -> User:
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

 
async def update_token(user: User, token: str | None, db: Session):
    user.refresh_token = token
    db.commit()

    
async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar_url(email: str, url: str | None, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user

