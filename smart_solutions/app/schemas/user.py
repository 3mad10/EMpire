from pydantic import BaseModel, HttpUrl, Field, EmailStr
from uuid import UUID
from typing import List, Optional


class UserCreate(BaseModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=256)
    phone_number: Optional[str] = Field(max_length=64)
    address: Optional[str] = Field(max_length=128)
    city: Optional[str] = Field(max_length=128)
    country: Optional[str] = Field()


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
