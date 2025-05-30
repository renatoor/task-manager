import uuid
from typing import Protocol

from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from uuid_extensions import uuid7


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    name: str
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str


class UserRepository(Protocol):
    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        """Create a user"""

    async def get_users(self) -> list[User]:
        """Get all users"""

    async def get_user_by_email(self, email: str) -> User | None:
        """Find a user by email"""

    async def get_user_by_id(self, id: uuid.UUID) -> User | None:
        """Find a user by id"""
