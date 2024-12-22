import redis
from config import settings


# Подключение к Redis
redis_db = redis.StrictRedis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    charset=settings.redis.charset,
    decode_responses=settings.redis.decode_responses,
    db=settings.redis.db
)
