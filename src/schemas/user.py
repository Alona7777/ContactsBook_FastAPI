from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from src.database.models import Role



class UserBase(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str 
    email: str
    role: Role

    class Config:
        from_attributes = True


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
