from sqlalchemy import text

from app.core.logger import logger
from app.db.session import SessionLocal
from app.services.cache_service import client as memcached_client


def perform_health_check() -> dict:
    db_status = "ok"
    cache_status = "ok"

    try:
        db = SessionLocal()
        result = db.execute(text("SELECT id FROM mms_data LIMIT 1"))
        db.close()

        if result.scalar() is None:
            raise Exception("No data in database")
    except Exception as e:
        logger.error("Error checking database connection", error=str(e))
        db_status = "error"

    try:
        memcached_client.set("health_check", b"1", expire=60, noreply=False)
        value = memcached_client.get("health_check")

        if value != b"1":
            raise ValueError("Cache mismatch")
    except Exception as e:
        logger.error("Memcached health check failed", error=str(e))
        cache_status = "error"

    status = "ok" if db_status == "ok" and cache_status == "ok" else "degraded"
    return {"status": status, "database": db_status, "cache": cache_status}
