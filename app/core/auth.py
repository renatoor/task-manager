from datetime import datetime, timedelta
from typing import Any

import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(
    data: dict[str, Any], expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    expires_at = datetime.utcnow() + timedelta(minutes=expires_delta)
    return jwt.encode({**data, "exp": expires_at}, SECRET_KEY, ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
