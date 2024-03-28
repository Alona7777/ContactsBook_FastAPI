from typing import List, Type

from datetime import date, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.user import UserBase, UserResponse

async def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user

async def create_user(body: UserBase, db: Session) -> User:
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

 
async def update_token(user: User, token: str | None, db: Session):
    user.refresh_token = token
    db.commit()

    