import uuid

from app.core.crypt import get_password_hash
from app.domain.user import User, UserRepository
from app.schemas.user import UserCreate


class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        return await self._user_repository.create_user(
            name=user.name, email=user.email, hashed_password=hashed_password
        )

    async def get_user_by_id(self, id: uuid.UUID) -> User:
        return await self._user_repository.get_user_by_id(id)

    async def get_user_by_email(self, email: str) -> User:
        return await self._user_repository.get_user_by_email(email)

    async def get_users(self) -> list[User]:
        return await self._user_repository.get_users()
