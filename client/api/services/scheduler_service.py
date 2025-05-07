from database import get_db
from datetime import datetime

class SchedulerService:
    def __init__(self):
        self._init_table()

    def _init_table(self):
        """初始化调度结果表"""
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS scheduler_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        db.commit()

    def get_results(self):
        """获取调度结果"""
        db = get_db()
        results = db.execute('''
            SELECT * FROM scheduler_results
            ORDER BY created_at DESC
            LIMIT 100
        ''').fetchall()
        return [dict(result) for result in results] 