import uuid
from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.task import Task
from app.domain.user import User


class SQLModelTaskRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_task(
        self, title: str, description: str, due_date: datetime, user_id: uuid.UUID
    ) -> Task:
        task = Task(
            title=title, description=description, due_date=due_date, user_id=user_id
        )

        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)

        return task

    async def get_task_by_id(self, id: uuid.UUID) -> Task | None:
        statement = select(Task).where(Task.id == id)
        result = await self._session.exec(statement)

        return result.first()

    async def update_task(
        self,
        id: uuid.UUID,
        title: str | None = None,
        description: str | None = None,
        due_date: datetime | None = None,
        completed: bool | None = None,
        user_id: uuid.UUID | None = None,
    ) -> Task:
        task = await self.get_task_by_id(id)

        if title:
            task.title = title

        if description:
            task.description = description

        if due_date:
            task.due_date = due_date

        if completed:
            task.completed = completed

        if user_id:
            task.user_id = user_id

        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)

        return task

    async def get_tasks(
        self,
        due_date: datetime | None = None,
        completed: bool | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[(Task, User)]:
        filters = [Task.user_id == User.id]

        if due_date:
            filters.append(Task.due_date <= due_date)

        if completed is not None:
            filters.append(Task.completed == completed)

        statement = select(Task, User).where(*filters).offset(offset).limit(limit)

        return await self._session.exec(statement)

    async def delete_task(self, task: Task):
        await self._session.delete(task)
        await self._session.commit()
