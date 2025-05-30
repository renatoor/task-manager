from app.core.dependencies import get_current_user, get_user_repository
from app.domain.user import User, UserRepository
from app.schemas.user import UserCreate, UserRead
from app.use_cases.user_usecase import UserUseCase
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


def get_user_usecase(user_repository: UserRepository = Depends(get_user_repository)):
    return UserUseCase(user_repository)


@router.post("/sign-up")
async def create_user(
    user_create: UserCreate, use_case: UserUseCase = Depends(get_user_usecase)
) -> UserRead:
    user = await use_case.get_user_by_email(user_create.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User '{user.email}' already exists",
        )

    user = await use_case.create_user(user_create)
    return UserRead(**user.model_dump())


@router.get("/me")
async def users_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead(**current_user.model_dump())


@router.get("/")
async def users(
    use_case: UserUseCase = Depends(get_user_usecase),
    current_user: User = Depends(get_current_user),
) -> list[UserRead]:
    users = await use_case.get_users()
    return [UserRead(**user.model_dump()) for user in users]
