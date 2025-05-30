import redis.asyncio as redis

from app.core.config import REDIS_URL

cache = redis.from_url(REDIS_URL, encoding="utf8")
