from flask import Blueprint, request, jsonify
from services.task_service import TaskService
from services.tag_service import TagService
from services.location_service import LocationService
import yaml
import os

bp = Blueprint('batch', __name__)

# 全局服务变量
task_service = None
tag_service = TagService()
location_service = LocationService()

def init_routes(task_svc):
    """初始化路由服务"""
    global task_service
    task_service = task_svc

# 加载配置
def load_config():
    # 获取项目根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_path = os.path.join(root_dir, 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()

@bp.route('/delete', methods=['POST'])
def batch_delete():
    """批量删除任务"""
    data = request.get_json()
    task_ids = data.get('task_ids', [])
    
    success_count = 0
    for task_id in task_ids:
        if task_service.delete_task(task_id):
            success_count += 1
    
    return jsonify({
        'success': True,
        'deleted_count': success_count,
        'total_count': len(task_ids)
    })

@bp.route('/tags', methods=['POST'])
def batch_update_tags():
    """批量更新任务标签"""
    data = request.get_json()
    task_ids = data.get('task_ids', [])
    tag_ids = data.get('tag_ids', [])
    
    success_count = 0
    for task_id in task_ids:
        if task_service.update_task_tags(task_id, tag_ids):
            success_count += 1
    
    return jsonify({
        'success': True,
        'updated_count': success_count,
        'total_count': len(task_ids)
    })

@bp.route('/locations', methods=['POST'])
def batch_update_locations():
    """批量更新任务位置"""
    data = request.get_json()
    task_ids = data.get('task_ids', [])
    location_id = data.get('location_id')
    
    success_count = 0
    for task_id in task_ids:
        if task_service.update_task_location(task_id, location_id):
            success_count += 1
    
    return jsonify({
        'success': True,
        'updated_count': success_count,
        'total_count': len(task_ids)
    })

@bp.route('/complete', methods=['POST'])
def batch_complete():
    """批量完成任务"""
    data = request.get_json()
    task_ids = data.get('task_ids', [])
    
    success_count = 0
    for task_id in task_ids:
        if task_service.complete_task(task_id):
            success_count += 1
    
    return jsonify({
        'success': True,
        'completed_count': success_count,
        'total_count': len(task_ids)
    })

@bp.route('/abandon', methods=['POST'])
def batch_abandon():
    """批量放弃任务"""
    data = request.get_json()
    task_ids = data.get('task_ids', [])
    
    success_count = 0
    for task_id in task_ids:
        if task_service.abandon_task(task_id):
            success_count += 1
    
    return jsonify({
        'success': True,
        'abandoned_count': success_count,
        'total_count': len(task_ids)
    })

@bp.route('/batch/tasks', methods=['POST'])
def batch_create_tasks():
    """批量创建任务"""
    try:
        tasks_data = request.get_json()
        if not tasks_data or not isinstance(tasks_data, list):
            return jsonify({'error': '无效的任务数据'}), 400
            
        results = []
        for task_data in tasks_data:
            try:
                task = task_service.create_task(task_data)
                results.append({
                    'success': True,
                    'task': task.model_dump()
                })
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e)
                })
                
        return jsonify({
            'message': f'成功处理 {len(results)} 个任务',
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 