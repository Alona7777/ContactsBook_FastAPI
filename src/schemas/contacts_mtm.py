from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, PastDate




class PhoneBase(BaseModel):
    phone: int 


class PhoneResponse(PhoneBase):
    id: int = 1

    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=20)
    email: EmailStr = Field(max_length=50)
    birth_date: date
    info: Optional[str] = None


class ContactResponse(ContactBase):
    id: int = 1
    phones: List[PhoneResponse] = []

    class Config:
        from_attributes = True

