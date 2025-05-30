import pytest
import pytest_asyncio
from app.core.dependencies import get_notification, get_session, rate_limit
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = "sqlite+aiosqlite://"


@pytest_asyncio.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: AsyncSession):
    def get_session_override():
        return session

    def no_op_dependency():
        pass

    class MockNotification:
        def send_email(email: str, content: str):
            pass

    app.dependency_overrides[rate_limit] = lambda *args, **kwargs: no_op_dependency
    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_notification] = lambda: MockNotification()

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
