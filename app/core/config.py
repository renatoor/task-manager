import os

POSTGRES_URL = os.getenv(
    "POSTGRES_URL", "postgresql+asyncpg://postgres:postgres@localhost/task_manager"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_BACKEND_URL = REDIS_URL
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
