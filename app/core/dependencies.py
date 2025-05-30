from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_limiter.depends import RateLimiter
from jwt.exceptions import InvalidTokenError
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import Annotated

from app.core.auth import decode_token
from app.core.database import engine
from app.domain.notification import Notification
from app.domain.task import TaskRepository
from app.domain.user import UserRepository
from app.infrastructure.celery_notification import CeleryNotification
from app.infrastructure.task_repository import SQLModelTaskRepository
from app.infrastructure.user_repository import SQLModelUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_notification() -> Notification:
    return CeleryNotification()


def get_user_repository(session: SessionDep) -> UserRepository:
    return SQLModelUserRepository(session)


def get_task_repository(session: SessionDep) -> TaskRepository:
    return SQLModelTaskRepository(session)


def rate_limit():
    return RateLimiter(times=10, seconds=5)


async def get_current_user(
    user_repository: UserRepository = Depends(get_user_repository),
    token: str = Depends(oauth2_scheme),
):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )

    try:
        payload = decode_token(token)
        email = payload.get("sub")

        if not email:
            raise exception

        user = await user_repository.get_user_by_email(email)

        if not user:
            raise exception

        return user
    except InvalidTokenError:
        raise exception
