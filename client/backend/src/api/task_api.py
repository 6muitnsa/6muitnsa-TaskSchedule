from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services import task_service
from utils.database import get_db
from schemas.task import Task, TaskCreate
from models.task import TaskStatus, TimeStatus

router = APIRouter()

@router.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    if len(task.name) > 100:
        raise HTTPException(status_code=400, detail="Task name cannot exceed 100 characters")
    if task.description and len(task.description) > 500:
        raise HTTPException(status_code=400, detail="Task description cannot exceed 500 characters")
    if task.status not in [TaskStatus.PENDING, TaskStatus.COMPLETED, TaskStatus.FOLLOW_UP, TaskStatus.CANCELLED]:
        raise HTTPException(status_code=400, detail="Invalid task status")
    if task.timeStatus not in [TimeStatus.NOT_STARTED, TimeStatus.IN_PROGRESS, TimeStatus.OVERDUE, TimeStatus.COMPLETED]:
        raise HTTPException(status_code=400, detail="Invalid time status")
    return task_service.create_task(db, task.dict())

@router.get("/tasks/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if limit > 1000:
        raise HTTPException(status_code=400, detail="Query limit cannot exceed 1000")
    tasks = task_service.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: str, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskCreate, db: Session = Depends(get_db)):
    if len(task.name) > 100:
        raise HTTPException(status_code=400, detail="Task name cannot exceed 100 characters")
    if task.description and len(task.description) > 500:
        raise HTTPException(status_code=400, detail="Task description cannot exceed 500 characters")
    if task.status not in [TaskStatus.PENDING, TaskStatus.COMPLETED, TaskStatus.FOLLOW_UP, TaskStatus.CANCELLED]:
        raise HTTPException(status_code=400, detail="Invalid task status")
    if task.timeStatus not in [TimeStatus.NOT_STARTED, TimeStatus.IN_PROGRESS, TimeStatus.OVERDUE, TimeStatus.COMPLETED]:
        raise HTTPException(status_code=400, detail="Invalid time status")
    task = task_service.update_task(db, task_id, task.dict())
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/status")
def update_task_status(task_id: str, status: str, db: Session = Depends(get_db)):
    if status not in [TaskStatus.PENDING, TaskStatus.COMPLETED, TaskStatus.FOLLOW_UP, TaskStatus.CANCELLED]:
        raise HTTPException(status_code=400, detail="Invalid task status")
    task = task_service.update_task_status(db, task_id, status)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task 