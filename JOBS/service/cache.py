import redis
from ..config import settings


redis_client = redis.Redis(
    host=settings.redis_hostname,
    port=settings.redis_port,
    db=0,
    decode_responses=True
)
print(redis_client.ping())
