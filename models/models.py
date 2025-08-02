from sqlalchemy import Column, Integer, String, DateTime
from db import Base
import datetime

class ActivityPeriod(Base):
    __tablename__ = 'activity_periods'

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String)  # e.g., "Reading" or "Not Reading"