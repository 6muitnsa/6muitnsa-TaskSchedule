from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LocalTask(Base):
    __tablename__ = "local_tasks"

    task_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer, default=0)
    status = Column(String, default="pending")
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sync_status = Column(String, default="pending")  # pending, synced, failed
    last_sync = Column(DateTime)
    tags = relationship("LocalTaskTag", back_populates="task")

class LocalTaskTag(Base):
    __tablename__ = "local_task_tags"

    id = Column(Integer, primary_key=True)
    task_id = Column(String, ForeignKey("local_tasks.task_id"))
    tag = Column(String, nullable=False)
    task = relationship("LocalTask", back_populates="tags")

class LocalPomodoro(Base):
    __tablename__ = "local_pomodoros"

    pomodoro_id = Column(String, primary_key=True)
    task_id = Column(String, ForeignKey("local_tasks.task_id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration = Column(Integer)  # 分钟
    type = Column(String)  # focus 或 rest
    completed = Column(Boolean, default=False)
    sync_status = Column(String, default="pending")
    last_sync = Column(DateTime)

class SyncQueue(Base):
    __tablename__ = "sync_queue"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String)  # task 或 pomodoro
    entity_id = Column(String)
    action = Column(String)  # create, update, delete
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    retry_count = Column(Integer, default=0)
    last_error = Column(String) 