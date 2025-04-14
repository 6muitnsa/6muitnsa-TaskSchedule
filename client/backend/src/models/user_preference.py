from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from .task import Base

class UserPreference(Base):
    __tablename__ = 'user_preferences'

    id = Column(String(36), primary_key=True)
    preferredAlgorithm = Column(String(50))
    timeSlice = Column(Integer)
    notificationSettings = Column(String(500))
    themeSettings = Column(String(500))
    createTime = Column(DateTime, nullable=False, default=datetime.utcnow)
    updateTime = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 