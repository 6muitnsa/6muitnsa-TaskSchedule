from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.task import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(String(36), primary_key=True)
    taskId = Column(String(36), ForeignKey('tasks.id'), nullable=False)
    startTime = Column(DateTime, nullable=False)
    endTime = Column(DateTime, nullable=False)
    actualDuration = Column(Integer, nullable=False)
    algorithm = Column(String(50), nullable=False)
    createTime = Column(DateTime, nullable=False, default=datetime.utcnow)

    task = relationship("Task", back_populates="schedules") 