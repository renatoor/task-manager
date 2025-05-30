import uuid
from datetime import datetime
from typing import Protocol

from sqlmodel import Field, SQLModel
from uuid_extensions import uuid7

from app.domain.user import User


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    title: str
    description: str
    completed: bool = Field(default=False)
    due_date: datetime
    user_id: uuid.UUID = Field(foreign_key="users.id")


class TaskRepository(Protocol):
    async def create_task(
        self, title: str, description: str, due_date: datetime, user_id: uuid.UUID
    ) -> Task:
        """Create a task"""

    async def get_task_by_id(self, id: uuid.UUID) -> Task | None:
        """Find a user by id"""

    async def update_task(
        self,
        id: uuid.UUID,
        title: str | None = None,
        description: str | None = None,
        due_date: datetime | None = None,
        completed: bool | None = None,
        user_id: uuid.UUID | None = None,
    ) -> Task:
        """Update a task"""

    async def get_tasks(
        self,
        due_date: datetime | None = None,
        completed: bool | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[(Task, User)]:
        """Get tasks filtered and paginated"""

    async def delete_task(self, task: Task):
        """Delete a task by id"""
