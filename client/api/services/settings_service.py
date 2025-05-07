import os
import json
from typing import Dict, Any

class SettingsService:
    def __init__(self):
        self.settings_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'settings.json')
        self._ensure_settings_file()

    def _ensure_settings_file(self):
        """确保设置文件存在"""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        if not os.path.exists(self.settings_file):
            self._save_settings({
                'paths': {
                    'data_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'),
                    'logs_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs'),
                    'backup_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
                },
                'scheduler': {
                    'enabled': True,
                    'interval': 300,  # 5分钟
                    'max_retries': 3
                },
                'notifications': {
                    'enabled': True,
                    'sound': True,
                    'desktop': True
                },
                'theme': 'light',
                'language': 'zh_CN'
            })

    def _load_settings(self) -> Dict:
        """加载设置"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_settings(self, settings: Dict):
        """保存设置"""
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)

    def get_path(self) -> Dict[str, str]:
        """获取路径设置"""
        settings = self._load_settings()
        return settings.get('paths', {
            'data_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'),
            'logs_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs'),
            'backup_dir': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
        })

    def update_path(self, paths: Dict[str, str]) -> Dict[str, str]:
        """更新路径设置"""
        settings = self._load_settings()
        settings['paths'] = paths
        self._save_settings(settings)
        return paths

    def get_all_settings(self) -> Dict[str, Any]:
        """获取所有设置"""
        return self._load_settings()

    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """更新设置"""
        current_settings = self._load_settings()
        current_settings.update(settings)
        self._save_settings(current_settings)
        return current_settings

    def get_setting(self, key: str, default: Any = None) -> Any:
        """获取特定设置"""
        settings = self._load_settings()
        return settings.get(key, default)

    def update_setting(self, key: str, value: Any) -> Any:
        """更新特定设置"""
        settings = self._load_settings()
        settings[key] = value
        self._save_settings(settings)
        return value 