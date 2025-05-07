from flask import Blueprint, request, jsonify
from database import get_db
import json
from datetime import datetime
from utils.response import success_response, error_response
from utils.logger import get_logger

bp = Blueprint('tasks', __name__)
logger = get_logger('task_routes')

def safe_get(data, *keys, default=None):
    """安全地获取嵌套字典中的值"""
    for key in keys:
        if not isinstance(data, dict):
            return default
        data = data.get(key, default)
        if data is None:
            return default
    return data

@bp.route('/', methods=['GET'])
def get_tasks():
    """获取任务列表"""
    try:
        logger.info('开始获取任务列表')
        db = get_db()
        search = request.args.get('search')
        tag = request.args.get('tag')
        location = request.args.get('location')
        status = request.args.get('status')
        
        logger.debug(f'查询参数: search={search}, tag={tag}, location={location}, status={status}')
        
        query = 'SELECT * FROM tasks WHERE 1=1'
        params = []
        
        if search:
            query += ' AND title LIKE ?'
            params.append(f'%{search}%')
        if tag:
            query += ' AND tags LIKE ?'
            params.append(f'%{tag}%')
        if location:
            query += ' AND location = ?'
            params.append(location)
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        logger.debug(f'执行SQL: {query} 参数: {params}')
        tasks = db.execute(query, params).fetchall()
        logger.info(f'成功获取任务列表，共{len(tasks)}条记录')
        
        return success_response(data=[dict(task) for task in tasks], message='获取任务列表成功')
    except Exception as e:
        logger.error(f'获取任务列表失败: {str(e)}', exc_info=True)
        return error_response(message=f'获取任务列表失败: {str(e)}')

@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """获取单个任务"""
    try:
        logger.info(f'开始获取任务，ID: {task_id}')
        db = get_db()
        task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if task is None:
            logger.warning(f'任务不存在，ID: {task_id}')
            return error_response(message='任务不存在', code=404)
        
        logger.info(f'成功获取任务，ID: {task_id}')
        return success_response(data=dict(task), message='获取任务成功')
    except Exception as e:
        logger.error(f'获取任务失败，ID: {task_id}, 错误: {str(e)}', exc_info=True)
        return error_response(message=f'获取任务失败: {str(e)}')

@bp.route('/', methods=['POST'])
def create_task():
    """创建任务"""
    try:
        data = json.loads(request.get_data())
        logger.info('开始创建任务')
        logger.debug(f'请求数据: {data}')
    except:
        logger.error('无效的请求数据', exc_info=True)
        return error_response(message='无效的请求数据', code=400)
        
    try:
        db = get_db()
        now = datetime.now().isoformat()
        cursor = db.execute('''
            INSERT INTO tasks (
                title, description, start_time, end_time, priority,
                tags, location, estimated_duration, commute_time, rest_time,
                period_type, period_value, completion_times_type,
                completion_times_value, time_slot_start, time_slot_end,
                status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name', ''),
            data.get('description', ''),
            data.get('startTime'),
            data.get('endTime'),
            data.get('priority', '中'),
            json.dumps(data.get('tags', []), ensure_ascii=False),
            data.get('location'),
            safe_get(data, 'timeInfo', 'estimatedDuration'),
            safe_get(data, 'timeInfo', 'commuteTime'),
            safe_get(data, 'timeInfo', 'restTime'),
            safe_get(data, 'complexInfo', 'period', 'type'),
            safe_get(data, 'complexInfo', 'period', 'value'),
            safe_get(data, 'complexInfo', 'completionTimes', 'type'),
            safe_get(data, 'complexInfo', 'completionTimes', 'value'),
            safe_get(data, 'complexInfo', 'timeSlot', 'start'),
            safe_get(data, 'complexInfo', 'timeSlot', 'end'),
            'pending',  # 设置默认状态
            now,
            now
        ))
        db.commit()
        
        task_id = cursor.lastrowid
        logger.info(f'成功创建任务，ID: {task_id}')
        
        return success_response(data={
            'id': task_id,
            'title': data.get('name', ''),
            'description': data.get('description', ''),
            'status': 'pending',
            'priority': data.get('priority', '中'),
            'startTime': data.get('startTime'),
            'endTime': data.get('endTime'),
            'tags': data.get('tags', []),
            'created_at': now,
            'updated_at': now
        }, message='创建任务成功')
    except Exception as e:
        logger.error(f'创建任务失败: {str(e)}', exc_info=True)
        return error_response(message=f'创建任务失败: {str(e)}')

@bp.route('/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    """更新任务状态"""
    try:
        data = json.loads(request.get_data())
        status = data.get('status')
        logger.info(f'开始更新任务状态，ID: {task_id}, 新状态: {status}')
        
        if not status:
            logger.warning(f'状态不能为空，ID: {task_id}')
            return error_response(message='状态不能为空', code=400)
            
        db = get_db()
        now = datetime.now().isoformat()
        db.execute('''
            UPDATE tasks 
            SET status = ?, updated_at = ?
            WHERE id = ?
        ''', (status, now, task_id))
        db.commit()
        
        logger.info(f'成功更新任务状态，ID: {task_id}')
        return success_response(message='更新任务状态成功')
    except Exception as e:
        logger.error(f'更新任务状态失败，ID: {task_id}, 错误: {str(e)}', exc_info=True)
        return error_response(message=f'更新任务状态失败: {str(e)}')

@bp.route('/<int:task_id>/priority', methods=['PATCH'])
def update_task_priority(task_id):
    """更新任务优先级"""
    try:
        data = json.loads(request.get_data())
        priority = data.get('priority')
        logger.info(f'开始更新任务优先级，ID: {task_id}, 新优先级: {priority}')
        
        if not priority:
            logger.warning(f'优先级不能为空，ID: {task_id}')
            return error_response(message='优先级不能为空', code=400)
            
        db = get_db()
        now = datetime.now().isoformat()
        db.execute('''
            UPDATE tasks 
            SET priority = ?, updated_at = ?
            WHERE id = ?
        ''', (priority, now, task_id))
        db.commit()
        
        logger.info(f'成功更新任务优先级，ID: {task_id}')
        return success_response(message='更新任务优先级成功')
    except Exception as e:
        logger.error(f'更新任务优先级失败，ID: {task_id}, 错误: {str(e)}', exc_info=True)
        return error_response(message=f'更新任务优先级失败: {str(e)}')

@bp.route('/<int:task_id>/tags', methods=['PATCH'])
def update_task_tags(task_id):
    """更新任务标签"""
    try:
        data = json.loads(request.get_data())
        tags = data.get('tags')
        logger.info(f'开始更新任务标签，ID: {task_id}, 新标签: {tags}')
        
        if not isinstance(tags, list):
            logger.warning(f'标签必须是数组，ID: {task_id}')
            return error_response(message='标签必须是数组', code=400)
            
        db = get_db()
        now = datetime.now().isoformat()
        db.execute('''
            UPDATE tasks 
            SET tags = ?, updated_at = ?
            WHERE id = ?
        ''', (json.dumps(tags, ensure_ascii=False), now, task_id))
        db.commit()
        
        logger.info(f'成功更新任务标签，ID: {task_id}')
        return success_response(message='更新任务标签成功')
    except Exception as e:
        logger.error(f'更新任务标签失败，ID: {task_id}, 错误: {str(e)}', exc_info=True)
        return error_response(message=f'更新任务标签失败: {str(e)}')

@bp.route('/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """完成任务"""
    try:
        data = json.loads(request.get_data())
        actual_time = data.get('actual_time')
        logger.info(f'开始完成任务，ID: {task_id}, 实际用时: {actual_time}')
        
        db = get_db()
        now = datetime.now().isoformat()
        db.execute('''
            UPDATE tasks 
            SET status = 'completed', 
                actual_time = ?,
                completed_at = ?,
                updated_at = ?
            WHERE id = ?
        ''', (actual_time, now, now, task_id))
        db.commit()
        
        logger.info(f'成功完成任务，ID: {task_id}')
        return success_response(message='完成任务成功')
    except Exception as e:
        logger.error(f'完成任务失败，ID: {task_id}, 错误: {str(e)}', exc_info=True)
        return error_response(message=f'完成任务失败: {str(e)}')

@bp.route('/<int:task_id>/abandon', methods=['POST'])
def abandon_task(task_id):
    """放弃任务"""
    try:
        logger.info(f'开始放弃任务，ID: {task_id}')
        db = get_db()
        now = datetime.now().isoformat()
        db.execute('''
            UPDATE tasks 
            SET status = 'abandoned', 
                abandoned_at = ?,
                updated_at = ?
            WHERE id = ?
        ''', (now, now, task_id))
        db.commit()
        
        logger.info(f'成功放弃任务，ID: {task_id}')
        return success_response(message='放弃任务成功')
    except Exception as e:
        logger.error(f'放弃任务失败，ID: {task_id}, 错误: {str(e)}', exc_info=True)
        return error_response(message=f'放弃任务失败: {str(e)}')

# ... 其他任务相关路由 