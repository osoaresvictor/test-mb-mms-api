from datetime import datetime, timedelta, timezone
from typing import List, cast

import cloudscraper
import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import ALLOWED_PAIRS, MB_API_BASE_URL
from app.core.constants import INITIAL_LOAD_DAYS_BACK, MMS_WINDOWS
from app.core.logger import logger
from app.db.session import SessionLocal
from app.models.candle_model import MMSData
from app.utils.mms_calculator import calculate_mms
from app.workers.incremental_loader import run_incremental_loader


@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(requests.RequestException),
)
def fetch_candles(pair: str, from_ts: int, to_ts: int) -> List[float]:
    url = f"{MB_API_BASE_URL}/v4/{pair}/candle"
    params = {"from": from_ts, "to": to_ts, "precision": "1d"}

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows"}
    )

    response = scraper.get(url, params=params)
    response.raise_for_status()
    return [float(c["close"]) for c in response.json()["candles"]]


def load_initial_data():
    db = SessionLocal()
    records_added: int = 0

    try:
        today = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        from_ts = int((today - timedelta(days=INITIAL_LOAD_DAYS_BACK)).timestamp())
        to_ts = int(today.timestamp())
        expected_days = INITIAL_LOAD_DAYS_BACK - max(MMS_WINDOWS) + 1

        for pair in ALLOWED_PAIRS:
            from_date = today - timedelta(days=expected_days - 1)
            existing_count = (
                db.query(MMSData)
                .filter(
                    MMSData.pair == pair,
                    MMSData.timestamp >= int(from_date.timestamp()),
                    MMSData.timestamp <= int(today.timestamp()),
                )
                .count()
            )

            if existing_count >= expected_days:
                logger.info(
                    f"Skipping {pair}: already has {existing_count} MMS entries."
                )
                continue

            logger.info(f"Fetching candles for {pair}")
            closes: List[float] = fetch_candles(pair, from_ts, to_ts)

            mms_dict = {window: calculate_mms(closes, window) for window in MMS_WINDOWS}

            for i in range(len(closes)):
                if all(mms_dict[window][i] for window in MMS_WINDOWS):
                    day = (
                        datetime.fromtimestamp(from_ts, timezone.utc)
                        + timedelta(days=i)
                    ).replace(hour=0, minute=0, second=0, microsecond=0)
                    timestamp = int(day.timestamp())

                    exists = (
                        db.query(MMSData)
                        .filter_by(pair=pair, timestamp=timestamp)
                        .first()
                    )
                    if exists:
                        logger.debug(
                            f"Skipping existing record for {pair} at {timestamp}"
                        )
                        continue

                    record = MMSData(
                        pair=pair,
                        timestamp=timestamp,
                        mms_20=round(cast(float, mms_dict[20][i]), 2),
                        mms_50=round(cast(float, mms_dict[50][i]), 2),
                        mms_200=round(cast(float, mms_dict[200][i]), 2),
                    )
                    db.add(record)
                    records_added += 1

        db.commit()
        logger.info(
            f"Initial loader completed successfully. " f"Records added: {records_added}"
        )
    except Exception as e:
        logger.error("Error in initial loader", error=str(e))
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    load_initial_data()
    logger.info("Running incremental loader right after initial load...")
    run_incremental_loader()
