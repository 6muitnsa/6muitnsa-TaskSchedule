from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    priority: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str
    time_status: str
    type: Optional[str] = None
    cycle: Optional[str] = None
    estimated_time: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    count: int
    is_locked: bool
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True 