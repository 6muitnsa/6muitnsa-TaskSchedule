from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TagBase(BaseModel):
    """标签基础模型"""
    name: str = Field(..., description="标签名称")
    color: str = Field(..., description="标签颜色")

class TagCreate(TagBase):
    """创建标签模型"""
    pass

class TagUpdate(BaseModel):
    """更新标签模型"""
    name: Optional[str] = Field(None, description="标签名称")
    color: Optional[str] = Field(None, description="标签颜色")

class Tag(TagBase):
    """标签完整模型"""
    id: int = Field(..., description="标签ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True 