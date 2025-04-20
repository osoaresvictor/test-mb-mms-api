from sqlalchemy.orm import Session, InstrumentedAttribute, Query

from app.models.candle_model import MMSData


def fetch_mms_data(pair: str, from_ts: int, to_ts: int, range_days: int, db: Session):
    column: InstrumentedAttribute = getattr(MMSData, f"mms_{range_days}")
    query: Query = (
        db.query(MMSData.timestamp, column.label("mms"))
        .filter(
            MMSData.pair == pair,
            MMSData.timestamp >= from_ts,
            MMSData.timestamp <= to_ts,
        )
        .order_by(MMSData.timestamp)
    )
    return [{"timestamp": row.timestamp, "mms": row.mms} for row in query.all()]
