import uuid
from datetime import datetime

from app.api.v1.users import get_user_usecase
from app.core.dependencies import (
    get_current_user,
    get_notification,
    get_task_repository,
    rate_limit,
)
from app.domain.notification import Notification
from app.domain.task import TaskRepository
from app.domain.user import User
from app.schemas.task import TaskBase, TaskPatch, TaskRead
from app.schemas.user import UserRead
from app.use_cases.task_usecase import TaskUseCase
from app.use_cases.user_usecase import UserUseCase
from fastapi import APIRouter, Depends, HTTPException, Response, status


def get_task_usecase(task_repository: TaskRepository = Depends(get_task_repository)):
    return TaskUseCase(task_repository)


router = APIRouter()


@router.post("/")
async def create_task(
    task: TaskBase,
    use_case: TaskUseCase = Depends(get_task_usecase),
    current_user: User = Depends(get_current_user),
):
    user = UserRead(**current_user.model_dump())
    task = await use_case.create_task(task, current_user)
    return TaskRead(**task.model_dump(), user=user)


@router.get("/", dependencies=[Depends(rate_limit)])
async def tasks(
    due_date: datetime | None = None,
    completed: bool | None = None,
    offset: int = 0,
    limit: int = 10,
    use_case: TaskUseCase = Depends(get_task_usecase),
    _: User = Depends(get_current_user),
) -> list[TaskRead]:
    result = await use_case.get_tasks(due_date, completed, offset, limit)
    return [
        TaskRead(**task.model_dump(), user=user.model_dump()) for task, user in result
    ]


@router.get("/{task_id}")
async def task(
    task_id: uuid.UUID,
    task_usecase: TaskUseCase = Depends(get_task_usecase),
    user_usecase: UserUseCase = Depends(get_user_usecase),
):
    task = await task_usecase.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task '{task_id}' not found"
        )

    user = await user_usecase.get_user_by_id(task.user_id)
    return TaskRead(**task.model_dump(), user=user.model_dump())


@router.patch("/{task_id}")
async def patch_task(
    task_id: uuid.UUID,
    task_patch: TaskPatch,
    task_usecase: TaskUseCase = Depends(get_task_usecase),
    user_usecase: UserUseCase = Depends(get_user_usecase),
    notification: Notification = Depends(get_notification),
):
    task = await task_usecase.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task '{task_id}' not found"
        )

    user = await user_usecase.get_user_by_id(task.user_id)
    user_read = UserRead(**user.model_dump())

    if task_patch.user_id:
        user = await user_usecase.get_user_by_id(task_patch.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"User '{task_patch.user_id}' not found",
            )

        user_read = UserRead(**user.model_dump())

    task = await task_usecase.update_task(task_id, task_patch)

    if task_patch.user_id:
        notification.send_email(user_read.email, f"Task '{task.id}' assigned to you")

    return TaskRead(**task.model_dump(), user=user_read)


@router.delete("/{task_id}")
async def delete_task(
    task_id: uuid.UUID, task_usecase: TaskUseCase = Depends(get_task_usecase)
):
    task = await task_usecase.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task '{task_id}' not found"
        )

    await task_usecase.delete_task(task)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
