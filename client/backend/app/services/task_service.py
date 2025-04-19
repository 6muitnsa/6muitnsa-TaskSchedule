from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from ..models.task import Task, TaskStatus, TimeStatus
from ..schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: TaskCreate) -> Task:
        db_task = Task(
            **task.dict(),
            status=TaskStatus.PENDING,
            time_status=TimeStatus.NOT_STARTED
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_task(self, task_id: int) -> Optional[Task]:
        result = await self.db.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        time_status: Optional[TimeStatus] = None
    ) -> List[Task]:
        query = select(Task)
        if status:
            query = query.where(Task.status == status)
        if time_status:
            query = query.where(Task.time_status == time_status)
        
        result = await self.db.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        db_task = await self.get_task(task_id)
        if not db_task:
            return None

        update_data = task.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        db_task.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def delete_task(self, task_id: int) -> bool:
        result = await self.db.execute(
            delete(Task).where(Task.id == task_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        db_task = await self.get_task(task_id)
        if not db_task:
            return None

        db_task.status = status
        if status == TaskStatus.COMPLETED:
            db_task.completed_count += 1
            if db_task.completed_count >= db_task.total_count:
                db_task.time_status = TimeStatus.COMPLETED

        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update_task_priority(self, task_id: int, priority: int) -> Optional[Task]:
        db_task = await self.get_task(task_id)
        if not db_task:
            return None

        db_task.priority = priority
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task 