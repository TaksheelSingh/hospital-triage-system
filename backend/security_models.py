from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class SecurityLog(Base):
    __tablename__ = "security_logs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50))
    entity = Column(String(50))
    entity_id = Column(Integer)
    severity = Column(String(20))
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text)