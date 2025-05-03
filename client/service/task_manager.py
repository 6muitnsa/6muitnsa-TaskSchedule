from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models import LocalTask, LocalTaskTag
import uuid

class TaskManager:
    async def create_task(self, db: Session, task_data: Dict) -> Dict:
        task_id = str(uuid.uuid4())
        task = LocalTask(
            task_id=task_id,
            title=task_data["title"],
            description=task_data.get("description"),
            priority=task_data.get("priority", 0),
            status=task_data.get("status", "pending"),
            due_date=task_data.get("due_date"),
            sync_status="pending"
        )
        
        if "tags" in task_data:
            for tag in task_data["tags"]:
                task_tag = LocalTaskTag(task_id=task_id, tag=tag)
                db.add(task_tag)
        
        db.add(task)
        db.commit()
        db.refresh(task)
        return self._format_task(task)

    async def get_tasks(self, db: Session) -> List[Dict]:
        tasks = db.query(LocalTask).all()
        return [self._format_task(task) for task in tasks]

    async def get_task(self, db: Session, task_id: str) -> Dict:
        task = db.query(LocalTask).filter(LocalTask.task_id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return self._format_task(task)

    async def update_task(self, db: Session, task_id: str, task_data: Dict) -> Dict:
        task = db.query(LocalTask).filter(LocalTask.task_id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        for key, value in task_data.items():
            if key != "tags":
                setattr(task, key, value)
        
        if "tags" in task_data:
            # 删除旧标签
            db.query(LocalTaskTag).filter(LocalTaskTag.task_id == task_id).delete()
            # 添加新标签
            for tag in task_data["tags"]:
                task_tag = LocalTaskTag(task_id=task_id, tag=tag)
                db.add(task_tag)
        
        task.sync_status = "pending"
        db.commit()
        db.refresh(task)
        return self._format_task(task)

    async def delete_task(self, db: Session, task_id: str) -> Dict:
        task = db.query(LocalTask).filter(LocalTask.task_id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.query(LocalTaskTag).filter(LocalTaskTag.task_id == task_id).delete()
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}

    def _format_task(self, task: LocalTask) -> Dict:
        tags = [tag.tag for tag in task.tags]
        return {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "sync_status": task.sync_status,
            "last_sync": task.last_sync,
            "tags": tags
        } 