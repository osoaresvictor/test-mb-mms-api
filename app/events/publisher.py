import asyncio

from app.core.logger import logger
from app.events.listener import handle_event


# just an example
def publish_event(event_type: str, payload: dict):
    logger.info("Event published", type=event_type, payload=payload)
    asyncio.run(handle_event(event_type, payload))
