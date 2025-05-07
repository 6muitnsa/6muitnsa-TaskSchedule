from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NotificationBase(BaseModel):
    """通知基础模型"""
    task_id: int = Field(..., description="关联的任务ID")
    type: str = Field(..., description="通知类型")
    message: str = Field(..., description="通知消息")
    is_read: bool = Field(default=False, description="是否已读")

class NotificationCreate(NotificationBase):
    """创建通知模型"""
    pass

class NotificationUpdate(BaseModel):
    """更新通知模型"""
    is_read: Optional[bool] = Field(None, description="是否已读")

class Notification(NotificationBase):
    """通知完整模型"""
    id: int = Field(..., description="通知ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True 