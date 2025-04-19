from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..db.base_class import Base

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FOLLOW_UP = "follow_up"
    CANCELLED = "cancelled"

class TimeStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    OVERDUE = "overdue"
    COMPLETED = "completed"

class TaskType(str, enum.Enum):
    WORK = "work"
    STUDY = "study"
    LIFE = "life"
    OTHER = "other"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    time_status = Column(Enum(TimeStatus), default=TimeStatus.NOT_STARTED)
    task_type = Column(Enum(TaskType), nullable=True)
    is_locked = Column(Boolean, default=False)
    estimated_time = Column(Integer, nullable=True)  # in minutes
    location = Column(String, nullable=True)
    commute_time = Column(Integer, nullable=True)  # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 周期性任务相关字段
    is_periodic = Column(Boolean, default=False)
    period_type = Column(String, nullable=True)  # daily, weekly, monthly
    period_value = Column(Integer, nullable=True)  # 周期值
    period_days = Column(String, nullable=True)  # 用于存储每周的特定日期，如"1,3,5"表示周一、周三、周五

    # 任务计数
    total_count = Column(Integer, default=1)
    completed_count = Column(Integer, default=0) 