from app.core.auth import create_access_token
from app.core.crypt import verify_password
from app.core.dependencies import get_user_repository, rate_limit
from app.domain.user import UserRepository
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

router = APIRouter()


@router.post("/token", dependencies=[Depends(rate_limit)])
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: UserRepository = Depends(get_user_repository),
):
    user = await user_repository.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": user.email})

    return {"access_token": token}
