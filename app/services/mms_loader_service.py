from datetime import datetime, timezone
from typing import Callable, List, Optional, Dict, Any

from cloudscraper import CloudScraper, create_scraper
import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import ALLOWED_PAIRS, MB_API_BASE_URL
from app.core.constants import DEFAULT_MMS_DAYS_BACK, MMS_WINDOWS, SECONDS_IN_DAY
from app.core.logger import logger
from app.db.session import SessionLocal
from app.models.candle_model import MMSData
from app.utils.mms_calculator import calculate_incremental_mms


@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(requests.RequestException),
)
def fetch_closes(pair: str, days: int) -> List[float]:
    to_ts: int = int(datetime.now(timezone.utc).timestamp())
    from_ts: int = to_ts - days * SECONDS_IN_DAY

    url: str = f"{MB_API_BASE_URL}/v4/{pair}/candle"
    params: Dict[str, Any] = {"from": from_ts, "to": to_ts, "precision": "1d"}

    scraper: CloudScraper = create_scraper(
        browser={"browser": "chrome", "platform": "windows"}
    )

    response = scraper.get(url, params=params)
    response.raise_for_status()
    return [float(c["close"]) for c in response.json()["candles"]]


def run_incremental_loader(
    publish_event_fn: Optional[Callable[[str, dict], None]] = None,
):
    db = SessionLocal()
    records_added: int = 0

    try:
        for pair in ALLOWED_PAIRS:
            closes: List[float] = fetch_closes(pair, DEFAULT_MMS_DAYS_BACK)
            timestamp: int = int(
                datetime.now(timezone.utc)
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )

            exists: Optional[MMSData] = (
                db.query(MMSData).filter_by(pair=pair, timestamp=timestamp).first()
            )
            if exists:
                logger.info(f"Skipping existing MMS for {pair} at {timestamp}")
                continue

            mms_values = {
                window: value
                for window in MMS_WINDOWS
                if (value := calculate_incremental_mms(closes, window)) is not None
            }

            record: MMSData = MMSData(
                pair=pair,
                timestamp=timestamp,
                mms_20=mms_values[20],
                mms_50=mms_values[50],
                mms_200=mms_values[200],
            )
            db.add(record)
            db.commit()
            records_added += 1

            if publish_event_fn:
                publish_event_fn(
                    "mms_calculated", {"pair": pair, "timestamp": timestamp}
                )
                logger.info(f"Event published for {pair} at {timestamp}")

        logger.info(
            f"Incremental loader completed successfully. "
            f"Records added: {records_added}"
        )

    except Exception as e:
        logger.error("Error during incremental loader flow", error=str(e))
        db.rollback()
    finally:
        db.close()
