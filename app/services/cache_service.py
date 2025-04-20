import json
from typing import Optional, Any

from pymemcache.client.base import Client

from app.core.config import CACHE_HOST, CACHE_PORT
from app.core.logger import logger

client: Client = Client((CACHE_HOST, CACHE_PORT))


def get_cache(key: str) -> Optional[Any]:
    try:
        result = client.get(key)
        if result:
            return json.loads(result)
    except Exception as e:
        logger.warning("Failed to read from cache", key=key, error=str(e))
    return None


def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        client.set(key, json.dumps(value), expire=expire)
    except Exception as e:
        logger.warning("Failed to write to cache", key=key, error=str(e))
