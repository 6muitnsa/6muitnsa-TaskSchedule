from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ReminderBase(BaseModel):
    """提醒基础模型"""
    task_id: int = Field(..., description="关联的任务ID")
    type: str = Field(..., description="提醒类型：once(单次)、daily(每天)、weekly(每周)、monthly(每月)")
    time: datetime = Field(..., description="提醒时间")
    is_active: bool = Field(default=True, description="是否激活")

class ReminderCreate(ReminderBase):
    """创建提醒模型"""
    pass

class ReminderUpdate(BaseModel):
    """更新提醒模型"""
    type: Optional[str] = Field(None, description="提醒类型")
    time: Optional[datetime] = Field(None, description="提醒时间")
    is_active: Optional[bool] = Field(None, description="是否激活")

class Reminder(ReminderBase):
    """提醒完整模型"""
    id: int = Field(..., description="提醒ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True 