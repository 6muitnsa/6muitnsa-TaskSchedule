from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class LocationBase(BaseModel):
    """位置基础模型"""
    name: str = Field(..., description="位置名称")
    address: str = Field(..., description="详细地址")
    latitude: float = Field(..., description="纬度")
    longitude: float = Field(..., description="经度")

class LocationCreate(LocationBase):
    """创建位置模型"""
    pass

class LocationUpdate(BaseModel):
    """更新位置模型"""
    name: Optional[str] = Field(None, description="位置名称")
    address: Optional[str] = Field(None, description="详细地址")
    latitude: Optional[float] = Field(None, description="纬度")
    longitude: Optional[float] = Field(None, description="经度")

class Location(LocationBase):
    """位置完整模型"""
    id: int = Field(..., description="位置ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True 