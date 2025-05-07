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

    def get_all_tasks(self):
        """获取所有任务"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks 
                ORDER BY created_at DESC
            ''')
            tasks = cursor.fetchall()
            return [dict(task) for task in tasks]
        except Exception as e:
            print(f"获取任务列表失败: {str(e)}")
            return []

    def get_task(self, task_id):
        """获取单个任务"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            return dict(task) if task else None
        except Exception as e:
            print(f"获取任务失败: {str(e)}")
            return None

    def create_task(self, data):
        """创建任务"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # 生成任务ID
            task_id = f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # 准备数据
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task_data = {
                'id': task_id,
                'title': data.get('name', ''),
                'description': data.get('description', ''),
                'priority': data.get('priority', '中'),
                'status': 'pending',
                'start_time': data.get('startTime'),
                'end_time': data.get('endTime'),
                'tags': ','.join(data.get('tags', [])),
                'created_at': now,
                'updated_at': now
            }
            
            # 插入数据
            cursor.execute('''
                INSERT INTO tasks (
                    id, title, description, priority, status,
                    start_time, end_time, tags, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task_data['id'],
                task_data['title'],
                task_data['description'],
                task_data['priority'],
                task_data['status'],
                task_data['start_time'],
                task_data['end_time'],
                task_data['tags'],
                task_data['created_at'],
                task_data['updated_at']
            ))
            
            conn.commit()
            return task_data
        except Exception as e:
            print(f"创建任务失败: {str(e)}")
            return None

    def update_task(self, task_id, data):
        """更新任务"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # 准备更新数据
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_data = {
                'title': data.get('name', ''),
                'description': data.get('description', ''),
                'priority': data.get('priority', '中'),
                'start_time': data.get('startTime'),
                'end_time': data.get('endTime'),
                'tags': ','.join(data.get('tags', [])),
                'updated_at': now
            }
            
            # 更新数据
            cursor.execute('''
                UPDATE tasks SET
                    title = ?,
                    description = ?,
                    priority = ?,
                    start_time = ?,
                    end_time = ?,
                    tags = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (
                update_data['title'],
                update_data['description'],
                update_data['priority'],
                update_data['start_time'],
                update_data['end_time'],
                update_data['tags'],
                update_data['updated_at'],
                task_id
            ))
            
            conn.commit()
            return self.get_task(task_id)
        except Exception as e:
            print(f"更新任务失败: {str(e)}")
            return None

    def delete_task(self, task_id):
        """删除任务"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"删除任务失败: {str(e)}")
            return False

    def update_task_tags(self, task_id, tag_ids):
        """更新任务标签"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # 首先删除现有的标签关联
            cursor.execute('DELETE FROM task_tags WHERE task_id = ?', (task_id,))
            
            # 添加新的标签关联
            for tag_id in tag_ids:
                cursor.execute('INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)',
                             (task_id, tag_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"更新任务标签失败: {str(e)}")
            return False

    def update_task_location(self, task_id, location_id):
        """更新任务位置"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # 获取地点名称
            cursor.execute("SELECT name FROM locations WHERE id = ?", (location_id,))
            location = cursor.fetchone()
            if not location:
                return False
            
            # 更新任务表中的地点字段
            cursor.execute("UPDATE tasks SET location = ? WHERE id = ?", 
                         (location['name'], task_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"更新任务位置失败: {str(e)}")
            return False

    def complete_task(self, task_id, actual_time=None):
        """完成任务"""
        try:
            conn = get_db()
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
            return True
        except Exception as e:
            print(f"完成任务失败: {str(e)}")
            return False

    def abandon_task(self, task_id):
        """放弃任务"""
        try:
            conn = get_db()
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
            return True
        except Exception as e:
            print(f"放弃任务失败: {str(e)}")
            return False

    def __del__(self):
        """关闭数据库连接"""
        if hasattr(self, 'conn'):
            self.conn.close()
