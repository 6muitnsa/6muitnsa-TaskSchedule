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
from database import init_db
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
    remote_routes  # 添加新的路由模块
)
import logging

# 初始化配置
Config.init()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Config.LOG_FILE)
    ]
)

# 创建应用
app = Flask(__name__)

# 配置 CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5173", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# 初始化数据库
init_db()

# 获取数据库路径
DB_PATH = Config.DATABASE_PATH

# 初始化服务
task_service = TaskService(DB_PATH)
statistics_service = StatisticsService(DB_PATH)
scheduler_service = SchedulerService()
settings_service = SettingsService()
sync_service = SyncService()
import_export_service = ImportExportService(DB_PATH)

# 初始化路由
statistics_routes.init_routes(statistics_service)
batch_routes.init_routes(task_service)  # 初始化batch_routes的服务

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
app.register_blueprint(remote_routes.sync_bp)  # 注册同步路由

# 任务相关路由
@app.route('/api/tasks/', methods=['GET'])
def get_tasks():
    return jsonify(task_service.get_all_tasks())

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    return jsonify(task_service.get_task(task_id))

@app.route('/api/tasks/', methods=['POST'])
def create_task():
    return jsonify(task_service.create_task(request.json))

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    return jsonify(task_service.update_task(task_id, request.json))

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    return jsonify(task_service.delete_task(task_id))

# 统计相关路由
@app.route('/api/statistics/overview', methods=['GET'])
def get_statistics_overview():
    return jsonify(statistics_service.get_overview())

@app.route('/api/statistics/daily', methods=['GET'])
def get_daily_statistics():
    date = request.args.get('date')
    return jsonify(statistics_service.get_daily_statistics(date))

@app.route('/api/statistics/weekly', methods=['GET'])
def get_weekly_statistics():
    return jsonify(statistics_service.get_weekly_statistics())

@app.route('/api/statistics/monthly', methods=['GET'])
def get_monthly_statistics():
    return jsonify(statistics_service.get_monthly_statistics())

# 设置相关路由
@app.route('/api/settings/path', methods=['GET'])
def get_settings_path():
    return jsonify(settings_service.get_path())

@app.route('/api/settings/path', methods=['PUT'])
def update_settings_path():
    return jsonify(settings_service.update_path(request.json))

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(settings_service.get_all_settings())

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    return jsonify(settings_service.update_settings(request.json))

# 同步相关路由
@app.route('/api/sync/status', methods=['GET'])
def get_sync_status():
    return jsonify(sync_service.get_status())

@app.route('/api/sync/start', methods=['POST'])
def start_sync():
    return jsonify(sync_service.start())

@app.route('/api/sync/stop', methods=['POST'])
def stop_sync():
    return jsonify(sync_service.stop())

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    ) 