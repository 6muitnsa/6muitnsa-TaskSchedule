import sqlite3
import os
import threading
from pathlib import Path
from config import Config

class DatabaseManager:
    """数据库管理器"""
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    def get_connection(self):
        """获取当前线程的数据库连接"""
        if not hasattr(self._local, 'connection'):
            db_path = Config.get_db_path()
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self._local.connection = sqlite3.connect(db_path, check_same_thread=False)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def close_connection(self):
        """关闭当前线程的数据库连接"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection

# 全局数据库管理器实例
db_manager = DatabaseManager()

def get_db():
    """获取数据库连接"""
    return db_manager.get_connection()

def close_db():
    """关闭数据库连接"""
    db_manager.close_connection()

def init_db():
    """初始化数据库"""
    db = get_db()
    cursor = db.cursor()
    
    # 创建任务表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending',
        due_date DATETIME,
        location TEXT,
        estimated_time INTEGER,
        tags TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建提醒表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        time DATETIME,
        type TEXT,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
    ''')
    
    # 创建标签表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        color TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建任务标签关联表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_tags (
        task_id INTEGER,
        tag_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (task_id, tag_id),
        FOREIGN KEY (task_id) REFERENCES tasks (id),
        FOREIGN KEY (tag_id) REFERENCES tags (id)
    )
    ''')
    
    # 创建位置表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建位置路由表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS location_routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_location_id INTEGER,
        to_location_id INTEGER,
        commute_time INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (from_location_id) REFERENCES locations (id),
        FOREIGN KEY (to_location_id) REFERENCES locations (id)
    )
    ''')
    
    # 创建任务位置关联表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_locations (
        task_id INTEGER,
        location_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (task_id, location_id),
        FOREIGN KEY (task_id) REFERENCES tasks (id),
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    ''')
    
    # 创建通知表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        type TEXT,
        message TEXT,
        status TEXT DEFAULT 'unread',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
    ''')
    
    # 创建同步记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sync_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        status TEXT,
        sync_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建番茄钟记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pomodoro_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        start_time DATETIME,
        duration INTEGER,
        status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
    ''')
    
    db.commit()
    print("数据库初始化完成")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d 