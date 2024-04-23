from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber as PydanticPhoneNumber

from src.schemas.user import UserResponse


PhoneNumber = type(
    "PhoneNumberStr",
    (PydanticPhoneNumber,),
    {   
        "default_region_code": "US",
        "phone_format": "E164",
    },
)


class ContactBase(BaseModel):
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=20)
    email: EmailStr = Field(max_length=50)
    phone: PhoneNumber
    birth_date: date | None
    info: Optional[str] = None


class ContactResponse(ContactBase):
    id: int = 1
    user_id: int | None

    model_config = ConfigDict(from_attributes = True)
    
    # class Config:
    #     from_attributes = True


class ContactResponseAdmin(ContactBase):
    id: int = 1
    user: UserResponse | None

    model_config = ConfigDict(from_attributes = True)

    # class Config:
    #     from_attributes = True

