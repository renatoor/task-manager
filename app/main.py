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

# import uuid
# from contextlib import asynccontextmanager
# from datetime import datetime, timedelta
#
# import jwt
# import redis.asyncio as redis
# from fastapi import Depends, FastAPI, HTTPException, Response, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi_limiter import FastAPILimiter
# from fastapi_limiter.depends import RateLimiter
# from passlib.context import CryptContext
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlmodel import SQLModel, select
# from sqlmodel.ext.asyncio.session import AsyncSession
# from typing_extensions import Annotated
#
# from .models import TaskModel, UserModel
# from .schemas import Task, TaskCreate, TaskUpdate, User, UserSignUp
#
# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager"
#
# engine = create_async_engine(DATABASE_URL, echo=True)
#
# SECRET_KEY = "super-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
#
#
# async def get_session():
#     async with AsyncSession(engine) as session:
#         yield session
#
#
# SessionDep = Annotated[AsyncSession, Depends(get_session)]
#
#
# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     await init_db()
#     redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
#     await FastAPILimiter.init(redis_connection)
#     yield
#     await FastAPILimiter.close()
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# app = FastAPI(lifespan=lifespan)
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     user_email = payload.get("sub")
#
#     if user_email and (
#         user_model := (
#             await session.exec(select(UserModel).where(UserModel.email == user_email))
#         ).first()
#     ):
#         return User(**user_model.dict())
# #
#     return HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
#     )
#
#
# @app.post("/sign-up")
# async def sign_in(user: UserSignUp, session: SessionDep):
#     hashed_password = pwd_context.hash(user.password)
#
#     user_model = UserModel(**user.dict(), hashed_password=hashed_password)
#
#     session.add(user_model)
#     await session.commit()
#     await session.refresh(user_model)
#
#     return User(**user_model.dict())
#
#
# @app.post("/token")
# async def token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
# ):
#     statement = select(UserModel).where(UserModel.email == form_data.username)
#     user = (await session.exec(statement)).first()
#
#     if not user or not pwd_context.verify(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#         )
#
#     expire_at = datetime.utcnow() + timedelta(minutes=30)
#     token = jwt.encode({"sub": user.email, "exp": expire_at}, SECRET_KEY, ALGORITHM)
#
#     return {"access_token": token}
#
#
# @app.get("/users/me")
# async def users_me(current_user: User = Depends(get_current_user)):
#     return current_user
#
#
# @app.get("/users")
# async def users(session: SessionDep, _: User = Depends(get_current_user)):
#     statement = select(UserModel)
#     users = await session.exec(statement)
#
#     return [User(**user_model.dict()) for user_model in users]
#
#
# @app.get("/tasks", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# async def tasks(
#     session: SessionDep,
#     offset: int = 0,
#     limit: int = 10,
#     _: User = Depends(get_current_user),
# ):
#     statement = (
#         select(TaskModel, UserModel)
#         .where(TaskModel.user_id == UserModel.id)
#         .offset(offset)
#         .limit(limit)
#     )
#     result = await session.exec(statement)
#     tasks = [Task(**task.dict(), user=user.dict()) for task, user in result]
#
#     return tasks
#
#
# @app.post("/tasks")
# async def create_task(
#     task: TaskCreate,
#     session: SessionDep,
#     current_user: User = Depends(get_current_user),
# ):
#     task_model = TaskModel(**task.dict(), user_id=current_user.id)
#
#     session.add(task_model)
#     await session.commit()
#     await session.refresh(task_model)
#
#     return task_model
#
#
# @app.patch("/tasks/{task_id}")
# async def patch_task(task_id: uuid.UUID, task_patch: TaskUpdate, session: SessionDep):
#     statement = select(TaskModel).where(TaskModel.id == task_id)
#     result = await session.exec(statement)
#     task = result.first()
#
#     if not task:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Task '{task_id}' not found"
#         )
#
#     if task_patch.user_id:
#         statement = select(UserModel).where(UserModel.id == task_patch.user_id)
#         result = await session.exec(statement)
#         user = result.first()
#
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 detail=f"User '{task_patch.user_id}' not found",
#             )
#
#     updated_data = task_patch.dict(exclude_none=True)
#
#     for field, value in updated_data.items():
#         setattr(task, field, value)
#
#     session.add(task)
#
#     await session.commit()
#     await session.refresh(task)
#
#     return task
#
#
# @app.delete("/tasks/{task_id}")
# async def delete_task(task_id: uuid.UUID, session: SessionDep):
#     statement = select(TaskModel).where(TaskModel.id == task_id)
#     result = await session.exec(statement)
#     task = result.first()
#
#     if not task:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Task '{task_id}' not found"
#         )
#
#     await session.delete(task)
#     await session.commit()
#
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
