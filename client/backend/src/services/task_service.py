from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from models.task import Task as TaskModel, TaskStatus, TimeStatus
from schemas.task import TaskCreate
from fastapi import HTTPException

def create_task(db: Session, task_data: dict) -> TaskModel:
    try:
        task = TaskModel(
            id=str(uuid.uuid4()),
            name=task_data['name'],
            description=task_data.get('description'),
            priority=task_data['priority'],
            start_time=task_data.get('start_time'),
            end_time=task_data.get('end_time'),
            status=TaskStatus.PENDING,
            time_status=TimeStatus.NOT_STARTED,
            type=task_data.get('type'),
            cycle=task_data.get('cycle'),
            count=0,
            is_locked=False,
            estimated_time=task_data.get('estimated_time'),
            create_time=datetime.utcnow(),
            update_time=datetime.utcnow()
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        print(f"Failed to create task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

def get_task(db: Session, task_id: str) -> TaskModel:
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return task
    except Exception as e:
        print(f"获取任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取任务失败: {str(e)}")

def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[TaskModel]:
    try:
        return db.query(TaskModel).offset(skip).limit(limit).all()
    except Exception as e:
        print(f"Failed to get tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get tasks: {str(e)}")

def update_task(db: Session, task_id: str, task_data: dict) -> TaskModel:
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        for key, value in task_data.items():
            setattr(task, key, value)
        task.update_time = datetime.utcnow()
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: str) -> bool:
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

def update_task_status(db: Session, task_id: str, status: str) -> TaskModel:
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        task.status = status
        task.update_time = datetime.utcnow()
        db.commit()
        db.refresh(task)
    return task 