from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class PeriodType(enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class TimeType(enum.Enum):
    FIXED = "fixed"
    FLEXIBLE = "flexible"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    priority = Column(Integer)  # 0-3000
    estimated_time = Column(Integer)  # 分钟
    location_id = Column(Integer, ForeignKey("locations.id"))
    period_type = Column(Enum(PeriodType))
    times = Column(Integer)  # 完成次数
    time_type = Column(Enum(TimeType))
    specific_time = Column(DateTime)  # 固定时间点
    start_time = Column(DateTime)  # 周期开始时间
    end_time = Column(DateTime)  # 周期结束时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    coordinates = Column(String)  # 经纬度坐标

class CommuteTime(Base):
    __tablename__ = "commute_times"

    id = Column(Integer, primary_key=True, index=True)
    from_location_id = Column(Integer, ForeignKey("locations.id"))
    to_location_id = Column(Integer, ForeignKey("locations.id"))
    default_minutes = Column(Integer, default=30)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    scheduler = Column(String, default="fcfs")
    time_granularity = Column(Integer, default=30)
    default_task_time = Column(Integer, default=60)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 