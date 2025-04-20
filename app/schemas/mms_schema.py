from pydantic import BaseModel


class MMSResponse(BaseModel):
    timestamp: int
    mms: float
