import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.user import User


class SQLModelUserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        user = User(name=name, email=email, hashed_password=hashed_password)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_users(self) -> list[User]:
        statement = select(User)
        return await self._session.exec(statement)

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self._session.exec(statement)
        return result.first()

    async def get_user_by_id(self, id: uuid.UUID) -> User | None:
        statement = select(User).where(User.id == id)
        result = await self._session.exec(statement)
        return result.first()
