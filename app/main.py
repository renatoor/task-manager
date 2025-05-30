from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from app.api.v1.auth import router as auth_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.users import router as users_router
from app.core.cache import cache
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    await FastAPILimiter.init(cache)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])
