import os
import yaml
from typing import Dict, Any
from pathlib import Path

class SettingsService:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'config.yaml')
        self._ensure_config_file()

    def _ensure_config_file(self):
        """确保配置文件存在"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        if not os.path.exists(self.config_file):
            self._save_config({
                'app': {
                    'name': '任务调度系统',
                    'debug': True,
                    'host': '127.0.0.1',
                    'port': 5000
                },
                'frontend': {
                    'host': '127.0.0.1',
                    'port': 5173
                },
                'database': {
                    'path': 'api/data/tasks.db',
                    'backup_path': 'api/data/backup'
                },
                'scheduler': {
                    'default_algorithm': 'FCFS',
                    'time_slice': 25,
                    'task_density': 'medium',
                    'daily_task_limit': 480
                },
                'pomodoro': {
                    'default_focus_time': 25,
                    'default_rest_time': 5,
                    'long_rest_time': 15,
                    'long_rest_interval': 4
                },
                'sync': {
                    'timeout': 300,
                    'qrcode_size': 200,
                    'max_retry': 3
                },
                'remote': {
                    'cloudflared_path': 'utils/Cloudflared/cloudflared-windows-386.exe',
                    'tunnel_wait_time': 6,
                    'temp_file_suffix': '.txt'
                },
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'file': 'logs/app.log',
                    'max_size': 10485760,
                    'backup_count': 5
                }
            })

    def _load_config(self) -> Dict:
        """加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return {}

    def _save_config(self, config: Dict):
        """保存配置"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # 打印调试信息
            print(f"正在保存配置到: {self.config_file}")
            print(f"配置内容: {config}")
            
            # 保存配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
                
            # 验证文件是否成功保存
            if os.path.exists(self.config_file):
                print(f"配置文件已成功保存到: {self.config_file}")
                # 读取保存的文件内容进行验证
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                    print(f"保存的文件内容: {saved_content}")
            else:
                raise Exception(f"配置文件保存失败: {self.config_file} 不存在")
                
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            print(f"当前工作目录: {os.getcwd()}")
            print(f"配置文件路径: {self.config_file}")
            raise

    def get_path(self) -> Dict[str, str]:
        """获取路径设置"""
        config = self._load_config()
        return {
            'data_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'),
            'logs_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs'),
            'backup_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
        }

    def update_path(self, paths: Dict[str, str]) -> Dict[str, str]:
        """更新路径设置"""
        config = self._load_config()
        config['database'] = {
            'path': paths['data_dir'],
            'backup_path': paths['backup_dir']
        }
        config['logging']['file'] = os.path.join(paths['logs_dir'], 'app.log')
        self._save_config(config)
        return paths

    def get_all_settings(self) -> Dict[str, Any]:
        """获取所有设置"""
        return self._load_config()

    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """更新设置"""
        try:
            # 确保配置文件存在
            self._ensure_config_file()
            
            # 加载当前配置
            config = self._load_config()
            print(f"当前配置: {config}")
            
            # 保留原有配置
            original_config = config.copy()
            
            # 更新调度设置
            if 'scheduler' in settings:
                if 'scheduler' not in config:
                    config['scheduler'] = {}
                config['scheduler'].update(settings['scheduler'])
                print(f"更新后的调度设置: {config['scheduler']}")
            
            # 更新优先级设置
            if 'priority' in settings:
                if 'priority' not in config:
                    config['priority'] = {}
                config['priority'].update(settings['priority'])
                print(f"更新后的优先级设置: {config['priority']}")
            
            # 更新时间预测设置
            if 'time_prediction' in settings:
                if 'time_prediction' not in config:
                    config['time_prediction'] = {}
                config['time_prediction'].update(settings['time_prediction'])
                print(f"更新后的时间预测设置: {config['time_prediction']}")
            
            # 更新番茄钟设置
            if 'pomodoro' in settings:
                if 'pomodoro' not in config:
                    config['pomodoro'] = {}
                config['pomodoro'].update(settings['pomodoro'])
                print(f"更新后的番茄钟设置: {config['pomodoro']}")
            
            # 更新同步设置
            if 'sync' in settings:
                if 'sync' not in config:
                    config['sync'] = {}
                config['sync'].update(settings['sync'])
                print(f"更新后的同步设置: {config['sync']}")
            
            # 更新日志设置
            if 'logging' in settings:
                if 'logging' not in config:
                    config['logging'] = {}
                config['logging'].update(settings['logging'])
                print(f"更新后的日志设置: {config['logging']}")
            
            # 恢复原有配置
            for key in ['app', 'frontend', 'database', 'remote']:
                if key in original_config:
                    config[key] = original_config[key]
            
            # 保存配置
            print(f"准备保存的完整配置: {config}")
            self._save_config(config)
            return config
        except Exception as e:
            print(f"更新设置失败: {str(e)}")
            raise

    def get_setting(self, key: str, default: Any = None) -> Any:
        """获取特定设置"""
        config = self._load_config()
        return config.get(key, default)

    def update_setting(self, key: str, value: Any) -> Any:
        """更新特定设置"""
        config = self._load_config()
        config[key] = value
        self._save_config(config)
        return value 