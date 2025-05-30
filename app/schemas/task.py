import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import UserRead


class TaskBase(BaseModel):
    title: str
    description: str
    due_date: datetime


class TaskRead(TaskBase):
    id: uuid.UUID
    user: UserRead
    completed: bool


class TaskPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    due_date: datetime | None = None
    user_id: uuid.UUID | None = None
