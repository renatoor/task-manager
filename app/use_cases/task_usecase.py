import uuid
from datetime import datetime

from app.domain.task import Task, TaskRepository
from app.domain.user import User
from app.schemas.task import TaskBase, TaskPatch


class TaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    async def create_task(self, task: TaskBase, user: User) -> Task:
        return await self._task_repository.create_task(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            user_id=user.id,
        )

    async def get_tasks(
        self,
        due_date: datetime | None = None,
        completed: bool | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[(Task, User)]:
        return await self._task_repository.get_tasks(due_date, completed, offset, limit)

    async def get_task_by_id(self, id: uuid.UUID) -> Task:
        return await self._task_repository.get_task_by_id(id)

    async def update_task(self, id: uuid.UUID, task_patch: TaskPatch) -> Task:
        return await self._task_repository.update_task(id, **task_patch.dict())

    async def delete_task(self, task: Task):
        return await self._task_repository.delete_task(task)
