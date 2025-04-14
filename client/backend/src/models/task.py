from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FOLLOW_UP = "FOLLOW_UP"
    CANCELLED = "CANCELLED"

class TimeStatus(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    OVERDUE = "OVERDUE"
    COMPLETED = "COMPLETED"

class Priority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    priority = Column(Integer, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    time_status = Column(SQLEnum(TimeStatus), nullable=False, default=TimeStatus.NOT_STARTED)
    type = Column(String(50))
    cycle = Column(String(50))
    count = Column(Integer, nullable=False, default=0)
    is_locked = Column(Boolean, nullable=False, default=False)
    estimated_time = Column(Integer)
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_time = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    schedules = relationship("Schedule", back_populates="task", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('priority IN (1, 2, 3)', name='check_priority'),
        CheckConstraint('count >= 0', name='check_count'),
        CheckConstraint('estimated_time >= 0', name='check_estimated_time'),
    ) 