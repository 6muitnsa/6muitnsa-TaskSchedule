from datetime import datetime
from database import get_db
from typing import Optional, List
from pydantic import BaseModel

class TaskCreate(BaseModel):
    """任务创建模型"""
    title: str
    description: Optional[str] = None
    status: str = 'pending'
    priority: str = 'medium'
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    commute_time: Optional[int] = None
    rest_time: Optional[int] = None
    period_type: Optional[str] = None
    period_value: Optional[int] = None
    completion_times_type: Optional[str] = None
    completion_times_value: Optional[int] = None
    time_slot_start: Optional[str] = None
    time_slot_end: Optional[str] = None
    location: Optional[str] = None

class Task:
    """任务模型"""
    def __init__(self, id=None, title=None, description=None, status='pending',
                 priority='medium', tags=None, due_date=None, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.tags = tags
        self.due_date = due_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @staticmethod
    def get_all():
        """获取所有任务"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tasks')
        return [Task(**dict(row)) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(task_id):
        """根据ID获取任务"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        return Task(**dict(row)) if row else None

    def save(self):
        """保存任务"""
        db = get_db()
        cursor = db.cursor()
        if self.id is None:
            # 创建新任务
            cursor.execute('''
                INSERT INTO tasks (title, description, status, priority, tags, due_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.title, self.description, self.status, self.priority,
                self.tags, self.due_date.isoformat() if self.due_date else None,
                self.created_at.isoformat(), self.updated_at.isoformat()
            ))
            self.id = cursor.lastrowid
        else:
            # 更新现有任务
            cursor.execute('''
                UPDATE tasks
                SET title = ?, description = ?, status = ?, priority = ?,
                    tags = ?, due_date = ?, updated_at = ?
                WHERE id = ?
            ''', (
                self.title, self.description, self.status, self.priority,
                self.tags, self.due_date.isoformat() if self.due_date else None,
                datetime.now().isoformat(), self.id
            ))
        db.commit()

    def delete(self):
        """删除任务"""
        if self.id is not None:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (self.id,))
            db.commit()

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'tags': self.tags,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 