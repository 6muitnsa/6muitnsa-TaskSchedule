import os
import yaml
from pathlib import Path

class Config:
    # 基础路径
    BASE_DIR = Path(__file__).parent.parent
    CONFIG_PATH = BASE_DIR / 'config' / 'config.yaml'
    
    # 默认配置
    APP_NAME = "任务调度系统"
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000
    DATABASE_PATH = str(BASE_DIR / "api" / "data" / "tasks.db")
    BACKUP_PATH = str(BASE_DIR / "api" / "data" / "backup")
    
    # 日志配置
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    
    # 系统配置
    SECRET_KEY = os.urandom(24)
    
    # 同步配置
    SYNC_TIMEOUT = 300  # 同步超时时间（秒）
    SYNC_QR_SIZE = 200  # 二维码大小
    
    # 调度配置
    DEFAULT_ALGORITHM = 'FCFS'  # 默认调度算法
    DEFAULT_TIME_SLICE = 25     # 默认时间片大小（分钟）
    
    # 番茄钟配置
    DEFAULT_FOCUS_TIME = 25     # 默认专注时间（分钟）
    DEFAULT_REST_TIME = 5       # 默认休息时间（分钟）
    
    @classmethod
    def init(cls):
        """初始化配置"""
        if cls.CONFIG_PATH.exists():
            with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
                # 应用配置
                app_config = config.get('app', {})
                cls.APP_NAME = app_config.get('name', cls.APP_NAME)
                cls.DEBUG = app_config.get('debug', cls.DEBUG)
                cls.HOST = app_config.get('host', cls.HOST)
                cls.PORT = app_config.get('port', cls.PORT)
                
                # 数据库配置
                db_config = config.get('database', {})
                cls.DATABASE_PATH = str(cls.BASE_DIR / db_config.get('path', "api/data/tasks.db"))
                cls.BACKUP_PATH = str(cls.BASE_DIR / db_config.get('backup_path', "api/data/backup"))
                
                # 确保目录存在
                os.makedirs(os.path.dirname(cls.DATABASE_PATH), exist_ok=True)
                os.makedirs(cls.BACKUP_PATH, exist_ok=True)
                
                # 创建必要的目录
                os.makedirs(cls.LOG_DIR, exist_ok=True) 