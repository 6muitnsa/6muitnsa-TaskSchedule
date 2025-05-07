import os
import yaml
from pathlib import Path
from typing import List, Dict, Any

class Config:
    """配置类"""
    _instance = None
    _initialized = False
    
    # 基础路径
    BASE_DIR = Path(__file__).parent.parent
    CONFIG_PATH = BASE_DIR / 'config' / 'config.yaml'
    
    # 配置数据
    _config = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
    
    @classmethod
    def init(cls):
        """初始化配置"""
        if cls.CONFIG_PATH.exists():
            with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
                cls._config = yaml.safe_load(f)
                
                # 确保目录存在
                os.makedirs(os.path.dirname(cls.get_db_path()), exist_ok=True)
                os.makedirs(cls.get_backup_path(), exist_ok=True)
                os.makedirs(os.path.dirname(cls.get_log_file()), exist_ok=True)
    
    @classmethod
    def get_app_name(cls) -> str:
        return cls._config.get('app', {}).get('name', '任务调度系统')
    
    @classmethod
    def get_debug(cls) -> bool:
        return cls._config.get('app', {}).get('debug', True)
    
    @classmethod
    def get_host(cls) -> str:
        return cls._config.get('app', {}).get('host', '127.0.0.1')
    
    @classmethod
    def get_port(cls) -> int:
        return cls._config.get('app', {}).get('port', 5000)
    
    @classmethod
    def get_db_path(cls) -> str:
        return str(cls.BASE_DIR / cls._config.get('database', {}).get('path', 'api/data/tasks.db'))
    
    @classmethod
    def get_backup_path(cls) -> str:
        return str(cls.BASE_DIR / cls._config.get('database', {}).get('backup_path', 'api/data/backup'))
    
    @classmethod
    def get_log_level(cls) -> str:
        return cls._config.get('logging', {}).get('level', 'INFO')
    
    @classmethod
    def get_log_format(cls) -> str:
        return cls._config.get('logging', {}).get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    @classmethod
    def get_log_file(cls) -> str:
        return str(cls.BASE_DIR / cls._config.get('logging', {}).get('file', 'logs/app.log'))
    
    @classmethod
    def get_log_max_size(cls) -> int:
        return cls._config.get('logging', {}).get('max_size', 10485760)  # 10MB
    
    @classmethod
    def get_log_backup_count(cls) -> int:
        return cls._config.get('logging', {}).get('backup_count', 5)
    
    @classmethod
    def get_scheduler_config(cls) -> Dict[str, Any]:
        return cls._config.get('scheduler', {})
    
    @classmethod
    def get_pomodoro_config(cls) -> Dict[str, Any]:
        return cls._config.get('pomodoro', {})
    
    @classmethod
    def get_sync_config(cls) -> Dict[str, Any]:
        return cls._config.get('sync', {})
    
    @classmethod
    def get_remote_config(cls) -> Dict[str, Any]:
        return cls._config.get('remote', {})
    
    @classmethod
    def get_cors_origins(cls) -> List[str]:
        frontend = cls._config.get('frontend', {})
        host = frontend.get('host', '127.0.0.1')
        port = frontend.get('port', 5173)
        return [f"http://{host}:{port}"]
    
    @classmethod
    def get_cors_methods(cls) -> List[str]:
        return ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
    
    @classmethod
    def get_cors_headers(cls) -> List[str]:
        return ['Content-Type', 'Authorization'] 