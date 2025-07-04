from pydantic import BaseModel, HttpUrl, Field, EmailStr, field_validator
from uuid import UUID
from typing import List, Optional
import re
from smart_solutions.app.core.config import settings


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=256)
    phone_number: Optional[str] = Field(max_length=64)
    address: Optional[str] = Field(max_length=128)
    city: Optional[str] = Field(max_length=128)
    country: Optional[str] = Field()

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v is None:
            return v
        # Simple international phone number format (e.g., +1234567890)
        phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
        if not phone_pattern.match(v):
            raise ValueError("Invalid phone number format.")
        return v

    @field_validator('country')
    def validate_country(cls, v):
        allowed_countries = settings.ALLOWED_COUNTRIES
        if v not in allowed_countries:
            raise ValueError(f"Country '{v}' is not in the list of allowed countries.")
        return v


class UserRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr = Field(max_length=255)
    is_admin: bool = False


class UserPublic(BaseModel):
    id: UUID
    name: str
    email: EmailStr = Field(max_length=255)
    is_admin: bool = False


class UserUpdate(BaseModel):
    name: Optional[str] = Field(max_length=255)
    email: Optional[EmailStr] = Field(max_length=255)
    phone_number: Optional[str] = Field(max_length=64)
    address: Optional[str] = Field(max_length=128)
    city: Optional[str] = Field(max_length=128)
    country: Optional[str] = Field()


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=256)
    new_password: str = Field(min_length=8, max_length=256)
