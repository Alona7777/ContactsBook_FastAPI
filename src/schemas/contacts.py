from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, PastDate, validator
from pydantic_extra_types.phone_numbers import PhoneNumber as PydanticPhoneNumber


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
    birth_date: date
    info: Optional[str] = None



class ContactResponse(ContactBase):
    id: int = 1

    class Config:
        from_attributes = True

