from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, PastDate




class PhoneBase(BaseModel):
    phone: int 


class PhoneResponse(PhoneBase):
    id: int

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=20)
    email: EmailStr = Field(max_length=50)
    birth_date: PastDate
    info: Optional[str] = None


class ContactResponse(ContactBase):
    id: int
    phones: List[PhoneResponse] = []

    class Config:
        orm_mode = True

