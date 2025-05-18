from sqlmodel import Field, SQLModel, Relationship
import uuid
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(nullable=False)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str = Field(nullable=False, min_length=8, max_length=256)

    phone_number: str = Field(nullable=True, max_length=64)
    address: str = Field(nullable=True, max_length=128)
    city: str = Field(nullable=True, max_length=128)
    country: str = Field(nullable=True)
    balance: int = Field(nullable=False, default=0)
    is_admin: bool = Field(nullable=False, default=False)
