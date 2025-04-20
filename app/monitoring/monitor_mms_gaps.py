from datetime import datetime, timedelta, timezone, date
from typing import Set

from app.core.config import ALLOWED_PAIRS
from app.core.constants import EXPECTED_MMS_DAYS_PER_PAIR
from app.core.logger import logger
from app.db.session import SessionLocal
from app.models.candle_model import MMSData


def monitor_gaps():
    db = SessionLocal()
    try:
        today: datetime = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        from_date: datetime = today - timedelta(days=EXPECTED_MMS_DAYS_PER_PAIR - 1)

        for pair in ALLOWED_PAIRS:
            result = db.query(MMSData.timestamp).filter(MMSData.pair == pair).all()

            actual_dates: Set[date] = {
                datetime.fromtimestamp(row[0], timezone.utc).date() for row in result
            }

            expected_dates: Set[date] = {
                (from_date + timedelta(days=i)).date()
                for i in range(EXPECTED_MMS_DAYS_PER_PAIR)
            }

            missing: Set[date] = expected_dates - actual_dates

            if missing:
                logger.warning(f"[{pair}] Missing {len(missing)} day(s) of MMS data.")
            else:
                logger.info(f"[{pair}] All good: No missing MMS data.")
    except Exception as e:
        logger.error("Error monitoring MMS", exc_info=e)
    finally:
        db.close()


if __name__ == "__main__":
    monitor_gaps()
