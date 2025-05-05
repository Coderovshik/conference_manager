import redis
import os

def get_redis():
    host = os.getenv("REDIS_HOST", "localhost")
    return redis.Redis(host=host, port=6379, db=0, decode_responses=True)