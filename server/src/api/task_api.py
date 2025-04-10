from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.services import task_service
from src.utils.database import get_db
from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

router = APIRouter()

class TaskCreate(BaseModel):
    name: str
    description: str = None
    priority: int = 1
    status: str = "待完成"
    time_status: str = "未开始"
    is_locked: bool = False

class TaskResponse(TaskCreate):
    id: str
    create_time: datetime
    update_time: datetime

    model_config = ConfigDict(from_attributes=True)

    @property
    def create_time_str(self) -> str:
        return self.create_time.isoformat() if self.create_time else None

    @property
    def update_time_str(self) -> str:
        return self.update_time.isoformat() if self.update_time else None

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task.model_dump())

@router.get("/tasks/", response_model=List[TaskResponse])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return task_service.list_tasks(db, skip, limit)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task: TaskCreate, db: Session = Depends(get_db)):
    updated_task = task_service.update_task(db, task_id, task.model_dump())
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"} 