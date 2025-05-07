from datetime import datetime
from typing import List, Optional
from models.notification import Notification, NotificationCreate, NotificationUpdate
from database import db_manager

class NotificationService:
    def __init__(self):
        pass

    def create_notification(self, notification: NotificationCreate) -> Notification:
        """创建通知"""
        now = datetime.now()
        notification_dict = notification.model_dump()
        notification_dict.update({
            'created_at': now,
            'updated_at': now
        })
        
        db = db_manager.get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO notifications (task_id, type, message, is_read, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            notification_dict['task_id'],
            notification_dict['type'],
            notification_dict['message'],
            notification_dict['is_read'],
            notification_dict['created_at'],
            notification_dict['updated_at']
        ))
        db.commit()
        
        notification_dict['id'] = cursor.lastrowid
        return Notification(**notification_dict)

    def get_notifications(self, task_id: Optional[int] = None) -> List[Notification]:
        """获取通知列表"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        if task_id:
            cursor.execute("""
                SELECT * FROM notifications 
                WHERE task_id = ? 
                ORDER BY created_at DESC
            """, (task_id,))
        else:
            cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC")
        
        notifications = cursor.fetchall()
        return [Notification(**dict(notification)) for notification in notifications]

    def get_notification(self, notification_id: int) -> Optional[Notification]:
        """获取单个通知"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM notifications WHERE id = ?", (notification_id,))
        notification = cursor.fetchone()
        return Notification(**dict(notification)) if notification else None

    def update_notification(self, notification_id: int, notification: NotificationUpdate) -> Optional[Notification]:
        """更新通知"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        updates = []
        values = []
        
        for field, value in notification.model_dump(exclude_unset=True).items():
            if value is not None:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return self.get_notification(notification_id)
        
        values.append(datetime.now())  # updated_at
        values.append(notification_id)
        
        query = f"""
            UPDATE notifications 
            SET {', '.join(updates)}, updated_at = ?
            WHERE id = ?
        """
        
        cursor.execute(query, values)
        db.commit()
        
        return self.get_notification(notification_id)

    def delete_notification(self, notification_id: int) -> bool:
        """删除通知"""
        db = db_manager.get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        db.commit()
        return cursor.rowcount > 0

    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """标记通知为已读"""
        return self.update_notification(
            notification_id,
            NotificationUpdate(is_read=True)
        ) 