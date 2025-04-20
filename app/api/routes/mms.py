from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.core.config import ALLOWED_PAIRS
from app.core.constants import MMS_WINDOWS
from app.db.session import get_db
from app.schemas.mms_schema import MMSResponse
from app.services.mms_service import get_mms_data

router = APIRouter()


@router.get("/{pair}/mms", response_model=List[MMSResponse], tags=["MMS"])
def read_mms(
    pair: str = Path(
        ..., description="Interest pair. Allowed: {}".format(ALLOWED_PAIRS)
    ),
    from_ts: int = Query(..., description="Start timestamp (Unix)"),
    to_ts: int = Query(..., description="End timestamp (Unix)"),
    range_days: int = Query(
        ..., description="Moving average window size {}".format(MMS_WINDOWS)
    ),
    db: Session = Depends(get_db),
) -> List[MMSResponse]:
    if pair not in ALLOWED_PAIRS:
        raise HTTPException(
            status_code=400,
            detail="Invalid 'pair' parameter. Must be one of {}".format(ALLOWED_PAIRS),
        )
    if range_days not in MMS_WINDOWS:
        raise HTTPException(
            status_code=400,
            detail="Invalid 'range_days' parameter. Must be {}".format(MMS_WINDOWS),
        )
    if from_ts > to_ts:
        raise HTTPException(
            status_code=400, detail="'from_ts' cannot be greater than 'to_ts'"
        )

    return get_mms_data(pair, from_ts, to_ts, range_days, db)
