from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from services.task_service import TaskService
from services.statistics_service import StatisticsService
from services.scheduler_service import SchedulerService
from services.settings_service import SettingsService
from services.sync_service import SyncService
from services.import_export_service import ImportExportService
from config import Config
from database import init_db, close_db
from routes import (
    task_routes,
    statistics_routes,
    import_export_routes,
    reminder_routes,
    scheduler_routes,
    settings_routes,
    pomodoro_routes,
    batch_routes,
    notification_routes,
    tag_routes,
    location_routes,
    sync_routes,
    remote_routes
)
import logging
from logging.handlers import RotatingFileHandler

# 初始化配置
Config.init()

# 配置日志
logging.basicConfig(
    level=getattr(logging, Config.get_log_level()),
    format=Config.get_log_format(),
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            Config.get_log_file(),
            maxBytes=Config.get_log_max_size(),
            backupCount=Config.get_log_backup_count()
        )
    ]
)

# 设置所有日志组件的级别
for logger_name in ['werkzeug', 'flask', 'sqlalchemy']:
    logging.getLogger(logger_name).setLevel(getattr(logging, Config.get_log_level()))

logger = logging.getLogger(__name__)

# 创建应用
app = Flask(__name__)

# 配置 CORS
CORS(app, resources={
    r"/api/*": {
        "origins": Config.get_cors_origins(),
        "methods": Config.get_cors_methods(),
        "allow_headers": Config.get_cors_headers(),
        "supports_credentials": True
    }
})

# 初始化数据库
logger.info("初始化数据库...")
init_db()

# 获取数据库路径
DB_PATH = Config.get_db_path()

# 初始化服务
task_service = TaskService(DB_PATH)
statistics_service = StatisticsService(DB_PATH)
scheduler_service = SchedulerService()
settings_service = SettingsService()
sync_service = SyncService()
import_export_service = ImportExportService(DB_PATH)

# 初始化路由
statistics_routes.init_routes(statistics_service)
batch_routes.init_routes(task_service)

# 注册路由
app.register_blueprint(task_routes.bp, url_prefix='/api/tasks')
app.register_blueprint(statistics_routes.bp, url_prefix='/api/statistics')
app.register_blueprint(import_export_routes.bp, url_prefix='/api/import_export')
app.register_blueprint(reminder_routes.bp, url_prefix='/api/reminder')
app.register_blueprint(scheduler_routes.bp, url_prefix='/api/scheduler')
app.register_blueprint(settings_routes.bp, url_prefix='/api/settings')
app.register_blueprint(pomodoro_routes.bp, url_prefix='/api/pomodoro')
app.register_blueprint(batch_routes.bp, url_prefix='/api/batch')
app.register_blueprint(notification_routes.bp, url_prefix='/api/notification')
app.register_blueprint(tag_routes.bp, url_prefix='/api/tags')
app.register_blueprint(location_routes.bp, url_prefix='/api/locations')
app.register_blueprint(sync_routes.bp, url_prefix='/api/sync')
app.register_blueprint(remote_routes.bp, url_prefix='/api/remote')
app.register_blueprint(remote_routes.sync_bp)

@app.teardown_appcontext
def teardown_db(exception=None):
    """请求结束时关闭数据库连接"""
    close_db()

logger.info("应用初始化完成")

if __name__ == '__main__':
    app.run(
        host=Config.get_host(),
        port=Config.get_port(),
        debug=Config.get_debug()
    ) 