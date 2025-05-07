from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from database import get_db

class SyncRecordBase(BaseModel):
    """同步记录基础模型"""
    device_id: str
    sync_time: datetime
    status: str
    details: str

class SyncRecordCreate(SyncRecordBase):
    """创建同步记录模型"""
    pass

class SyncRecord:
    """同步记录模型"""
    def __init__(self, id=None, device_id=None, sync_time=None, status='success',
                 details=None, created_at=None, updated_at=None):
        self.id = id
        self.device_id = device_id
        self.sync_time = sync_time or datetime.now()
        self.status = status
        self.details = details
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @staticmethod
    def get_all():
        """获取所有同步记录"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM sync_records')
        return [SyncRecord(**dict(row)) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(record_id):
        """根据ID获取同步记录"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM sync_records WHERE id = ?', (record_id,))
        row = cursor.fetchone()
        return SyncRecord(**dict(row)) if row else None

    def save(self):
        """保存同步记录"""
        db = get_db()
        cursor = db.cursor()
        if self.id is None:
            # 创建新记录
            cursor.execute('''
                INSERT INTO sync_records (device_id, sync_time, status, details, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.device_id, self.sync_time.isoformat(), self.status,
                self.details, self.created_at.isoformat(), self.updated_at.isoformat()
            ))
            self.id = cursor.lastrowid
        else:
            # 更新现有记录
            cursor.execute('''
                UPDATE sync_records
                SET device_id = ?, sync_time = ?, status = ?, details = ?, updated_at = ?
                WHERE id = ?
            ''', (
                self.device_id, self.sync_time.isoformat(), self.status,
                self.details, datetime.now().isoformat(), self.id
            ))
        db.commit()

    def delete(self):
        """删除同步记录"""
        if self.id is not None:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('DELETE FROM sync_records WHERE id = ?', (self.id,))
            db.commit()

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'sync_time': self.sync_time.isoformat(),
            'status': self.status,
            'details': self.details,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 