import sqlite3
import os
import threading
from config import Config
from datetime import datetime

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """获取当前线程的数据库连接"""
        if not hasattr(self._local, 'connection'):
            # 使用配置的数据库路径
            db_path = Config.DATABASE_PATH
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self._local.connection = sqlite3.connect(db_path)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def close_connection(self):
        """关闭当前线程的数据库连接"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection

# 创建全局数据库管理器实例
db_manager = DatabaseManager()

def get_db():
    """获取数据库连接"""
    return db_manager.get_connection()

def init_db():
    """初始化数据库"""
    db = get_db()
    cursor = db.cursor()
    
    # 删除旧表
    cursor.execute('DROP TABLE IF EXISTS tasks')
    cursor.execute('DROP TABLE IF EXISTS reminders')
    
    # 创建任务表
    cursor.execute('''
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        start_time TEXT,
        end_time TEXT,
        tags TEXT,
        location TEXT,
        estimated_duration INTEGER,
        commute_time INTEGER,
        rest_time INTEGER,
        period_type TEXT,
        period_value INTEGER,
        completion_times_type TEXT,
        completion_times_value INTEGER,
        time_slot_start TEXT,
        time_slot_end TEXT,
        actual_time INTEGER,
        completed_at TEXT,
        abandoned_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')
    
    # 创建提醒表
    cursor.execute('''
    CREATE TABLE reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        time TEXT NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
    )
    ''')
    
    # 创建标签表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        color TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')
    
    # 创建任务标签关联表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_tags (
        task_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        PRIMARY KEY (task_id, tag_id),
        FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
    )
    ''')
    
    # 创建位置表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')
    
    # 创建任务位置关联表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_locations (
        task_id INTEGER NOT NULL,
        location_id INTEGER NOT NULL,
        PRIMARY KEY (task_id, location_id),
        FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
        FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE
    )
    ''')
    
    # 创建通知表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read BOOLEAN NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
    )
    ''')
    
    # 创建同步记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sync_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sync_id TEXT NOT NULL,
        direction TEXT NOT NULL,
        status TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    ''')
    
    # 创建番茄钟记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pomodoro_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        duration INTEGER NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
    )
    ''')
    
    db.commit()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d 