from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    priority: int
    estimated_time: int
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_fixed_time: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    name: Optional[str] = None
    priority: Optional[int] = None
    estimated_time: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SettingsBase(BaseModel):
    scheduler: str = "fcfs"
    time_granularity: int = 30
    default_task_time: int = 60

class SettingsCreate(SettingsBase):
    pass

class SettingsUpdate(SettingsBase):
    scheduler: Optional[str] = None
    time_granularity: Optional[int] = None
    default_task_time: Optional[int] = None

class SettingsResponse(SettingsBase):
    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 