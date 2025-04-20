from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.config import ALLOWED_PAIRS
from app.core.constants import MMS_CACHE_TTL_SECONDS, MMS_WINDOWS, SECONDS_IN_DAY
from app.core.logger import logger
from app.db.crud import fetch_mms_data
from app.schemas.mms_schema import MMSResponse
from app.services.cache_service import get_cache, set_cache


def get_mms_data(
    pair: str, from_ts: int, to_ts: int, range_days: int, db: Session
) -> List[MMSResponse]:
    if pair not in ALLOWED_PAIRS:
        raise ValueError("Invalid pair")
    if range_days not in MMS_WINDOWS:
        raise ValueError("Invalid range")
    if from_ts > to_ts:
        raise ValueError("'from_ts' cannot be greater than 'to_ts'")

    normalized_from: int = from_ts - (from_ts % SECONDS_IN_DAY)
    normalized_to: int = to_ts - (to_ts % SECONDS_IN_DAY)
    cache_key: str = f"{pair}:{normalized_from}:{normalized_to}:{range_days}"

    now_ts: int = int(datetime.now(timezone.utc).timestamp())

    # Only cache results if the latest requested timestamp (to_ts)
    # is older than "now - 12 hours", to avoid caching potentially
    # incomplete daily candles
    safe_cache: bool = normalized_to < (now_ts - (SECONDS_IN_DAY // 2))

    if safe_cache:
        cached_result: Optional[List[MMSResponse]] = get_cache(cache_key)
        if cached_result:
            logger.info("Cache hit", key=cache_key)
            return cached_result
        logger.info("Cache miss, querying DB", key=cache_key)
    else:
        logger.info("Bypassing cache for fresh data", key=cache_key)

    result: List[MMSResponse] = fetch_mms_data(pair, from_ts, to_ts, range_days, db)

    if safe_cache:
        set_cache(cache_key, result, MMS_CACHE_TTL_SECONDS)

    return result
