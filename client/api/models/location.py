from datetime import datetime
from pydantic import BaseModel, Field

class LocationBase(BaseModel):
    """位置基础模型"""
    name: str = Field(..., description="位置名称")

class LocationCreate(LocationBase):
    """创建位置模型"""
    pass

class LocationUpdate(BaseModel):
    """更新位置模型"""
    name: str = Field(..., description="位置名称")

class Location(LocationBase):
    """位置完整模型"""
    id: int = Field(..., description="位置ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True 