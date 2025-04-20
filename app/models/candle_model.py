from sqlalchemy import Column, Float, Integer, String

from app.db.session import Base


class MMSData(Base):
    __tablename__ = "mms_data"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String, index=True)
    timestamp = Column(Integer, index=True)
    mms_20 = Column(Float)
    mms_50 = Column(Float)
    mms_200 = Column(Float)
