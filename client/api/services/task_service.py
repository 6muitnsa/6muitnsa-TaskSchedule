from database import get_db
from datetime import datetime
import sqlite3
import threading

class TaskService:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(TaskService, cls).__new__(cls)
                cls._instance.db_path = db_path
            return cls._instance

    def __init__(self, db_path):
        if not hasattr(self, 'initialized'):
            self.db_path = db_path
            self.initialized = True

    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all_tasks(self):
        """获取所有任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks 
                ORDER BY created_at DESC
            ''')
            tasks = cursor.fetchall()
            conn.close()
            return [dict(task) for task in tasks]
        except Exception as e:
            print(f"获取任务列表失败: {str(e)}")
            return []

    def get_task(self, task_id):
        """获取单个任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            conn.close()
            return dict(task) if task else None
        except Exception as e:
            print(f"获取任务失败: {str(e)}")
            return None

    def create_task(self, task_data):
        """创建任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (
                    title, description, status, priority,
                    start_time, end_time, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            ''', (
                task_data['title'],
                task_data.get('description', ''),
                task_data.get('status', 'pending'),
                task_data.get('priority', 'medium'),
                task_data.get('start_time'),
                task_data.get('end_time')
            ))
            conn.commit()
            task_id = cursor.lastrowid
            conn.close()
            return self.get_task(task_id)
        except Exception as e:
            print(f"创建任务失败: {str(e)}")
            return None

    def update_task(self, task_id, task_data):
        """更新任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            update_fields = []
            values = []
            for key, value in task_data.items():
                if key in ['title', 'description', 'status', 'priority', 'start_time', 'end_time']:
                    update_fields.append(f"{key} = ?")
                    values.append(value)
            
            if not update_fields:
                conn.close()
                return None
                
            values.append(task_id)
            cursor.execute(f'''
                UPDATE tasks 
                SET {', '.join(update_fields)}, updated_at = datetime('now')
                WHERE id = ?
            ''', values)
            conn.commit()
            conn.close()
            return self.get_task(task_id)
        except Exception as e:
            print(f"更新任务失败: {str(e)}")
            return None

    def delete_task(self, task_id):
        """删除任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除任务失败: {str(e)}")
            return False

    def update_task_tags(self, task_id, tag_ids):
        """更新任务标签"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 首先删除现有的标签关联
            cursor.execute('DELETE FROM task_tags WHERE task_id = ?', (task_id,))
            
            # 添加新的标签关联
            for tag_id in tag_ids:
                cursor.execute('INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)',
                             (task_id, tag_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新任务标签失败: {str(e)}")
            return False

    def update_task_location(self, task_id, location_id):
        """更新任务位置"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 首先删除现有的位置关联
            cursor.execute('DELETE FROM task_locations WHERE task_id = ?', (task_id,))
            
            # 添加新的位置关联
            cursor.execute('INSERT INTO task_locations (task_id, location_id) VALUES (?, ?)',
                          (task_id, location_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新任务位置失败: {str(e)}")
            return False

    def complete_task(self, task_id, actual_time=None):
        """完成任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute('''
                UPDATE tasks 
                SET status = 'completed',
                    actual_time = ?,
                    completed_at = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (actual_time, now, now, task_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"完成任务失败: {str(e)}")
            return False

    def abandon_task(self, task_id):
        """放弃任务"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute('''
                UPDATE tasks 
                SET status = 'abandoned',
                    abandoned_at = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (now, now, task_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"放弃任务失败: {str(e)}")
            return False

    def __del__(self):
        """关闭数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close()
