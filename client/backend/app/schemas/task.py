from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.task import TaskStatus, TimeStatus, TaskType

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    priority: int = Field(ge=0, le=3000)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    task_type: Optional[TaskType] = None
    is_locked: bool = False
    estimated_time: Optional[int] = None
    location: Optional[str] = None
    commute_time: Optional[int] = None

    # 周期性任务相关字段
    is_periodic: bool = False
    period_type: Optional[str] = None
    period_value: Optional[int] = None
    period_days: Optional[str] = None

    # 任务计数
    total_count: int = 1

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    name: Optional[str] = None
    priority: Optional[int] = Field(None, ge=0, le=3000)
    status: Optional[TaskStatus] = None
    time_status: Optional[TimeStatus] = None

class TaskInDB(TaskBase):
    id: int
    status: TaskStatus
    time_status: TimeStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_count: int = 0

    class Config:
        from_attributes = True

class TaskResponse(TaskInDB):
    pass

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    size: int 