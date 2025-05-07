from datetime import datetime, timedelta
from typing import List, Optional
from models.reminder import Reminder, ReminderCreate, ReminderUpdate
from database import db_manager
from services.notification_service import NotificationService

class ReminderService:
    def __init__(self):
        self.notification_service = NotificationService()

    def create_reminder(self, reminder: ReminderCreate) -> Reminder:
        """创建任务提醒"""
        now = datetime.now()
        reminder_dict = reminder.model_dump()
        reminder_dict.update({
            'created_at': now,
            'updated_at': now
        })
        
        db = db_manager.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO reminders (task_id, type, time, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            reminder_dict['task_id'],
            reminder_dict['type'],
            reminder_dict['time'],
            reminder_dict['is_active'],
            reminder_dict['created_at'],
            reminder_dict['updated_at']
        ))
        db.commit()
        
        reminder_dict['id'] = cursor.lastrowid
        return Reminder(**reminder_dict)

    def get_reminders(self, task_id: Optional[int] = None) -> List[Reminder]:
        """获取提醒列表"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        if task_id:
            cursor.execute("""
                SELECT * FROM reminders 
                WHERE task_id = ? 
                ORDER BY time ASC
            """, (task_id,))
        else:
            cursor.execute("SELECT * FROM reminders ORDER BY time ASC")
        
        reminders = cursor.fetchall()
        return [Reminder(**dict(reminder)) for reminder in reminders]

    def get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """获取单个提醒"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reminders WHERE id = ?", (reminder_id,))
        reminder = cursor.fetchone()
        return Reminder(**dict(reminder)) if reminder else None

    def update_reminder(self, reminder_id: int, reminder: ReminderUpdate) -> Optional[Reminder]:
        """更新提醒"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        updates = []
        values = []
        
        for field, value in reminder.model_dump(exclude_unset=True).items():
            if value is not None:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return self.get_reminder(reminder_id)
        
        values.append(datetime.now())  # updated_at
        values.append(reminder_id)
        
        query = f"""
            UPDATE reminders 
            SET {', '.join(updates)}, updated_at = ?
            WHERE id = ?
        """
        
        cursor.execute(query, values)
        db.commit()
        
        return self.get_reminder(reminder_id)

    def delete_reminder(self, reminder_id: int) -> bool:
        """删除提醒"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        db.commit()
        return cursor.rowcount > 0

    def check_reminders(self):
        """检查并触发提醒"""
        now = datetime.now()
        db = db_manager.get_connection()
        cursor = db.cursor()
        
        # 获取需要触发的提醒
        cursor.execute("""
            SELECT r.*, t.title as task_title 
            FROM reminders r
            JOIN tasks t ON r.task_id = t.id
            WHERE r.is_active = 1 
            AND r.time <= ?
            AND r.time > ?
        """, (now, now - timedelta(minutes=1)))
        
        reminders = cursor.fetchall()
        
        for reminder in reminders:
            # 创建通知
            self.notification_service.create_notification({
                'task_id': reminder['task_id'],
                'type': reminder['type'],
                'message': f"任务 '{reminder['task_title']}' 的提醒：{reminder['type']}"
            })
            
            # 如果是单次提醒，则禁用该提醒
            if reminder['type'] == 'once':
                self.update_reminder(
                    reminder['id'],
                    ReminderUpdate(is_active=False)
                ) 