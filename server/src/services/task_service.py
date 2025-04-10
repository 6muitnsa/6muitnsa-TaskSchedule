from sqlalchemy.orm import Session
from src.models.task import Task
import uuid
from datetime import datetime

def create_task(db: Session, task_data: dict):
    task = Task(
        id=str(uuid.uuid4()),
        name=task_data["name"],
        description=task_data.get("description"),
        priority=task_data.get("priority", 1),
        status=task_data.get("status", "待完成"),
        time_status=task_data.get("time_status", "未开始"),
        is_locked=task_data.get("is_locked", False)
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: str):
    return db.query(Task).filter(Task.id == task_id).first()

def list_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: str, task_data: dict):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        for key, value in task_data.items():
            setattr(task, key, value)
        task.update_time = datetime.now()
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False 