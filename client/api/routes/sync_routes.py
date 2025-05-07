from flask import Blueprint, request, jsonify
from database import get_db
import qrcode
import io
import base64
from datetime import datetime
import json
from services.sync_service import SyncService

bp = Blueprint('sync', __name__)
sync_service = SyncService()

@bp.route('/url', methods=['GET'])
def get_sync_url():
    # 生成同步URL
    sync_url = f"http://{request.host}/sync"
    return jsonify({
        'code': 200,
        'data': {
            'url': sync_url
        },
        'message': '获取同步URL成功'
    })

@bp.route('/qrcode', methods=['GET'])
def get_sync_qrcode():
    # 生成同步URL
    sync_url = f"http://{request.host}/sync"
    
    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(sync_url)
    qr.make(fit=True)
    
    # 创建二维码图片
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 转换为base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({
        'code': 200,
        'data': {
            'qrcode': f"data:image/png;base64,{img_str}"
        },
        'message': '获取同步二维码成功'
    })

@bp.route('/tasks', methods=['POST'])
def sync_tasks():
    data = request.get_json()
    db = get_db()
    
    # 记录同步
    now = datetime.now().isoformat()
    db.execute('''
        INSERT INTO sync_records (sync_id, direction, status, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (data['sync_id'], data['direction'], 'success', now))
    
    # 同步任务数据
    if data['direction'] == 'upload':
        # 上传数据到服务器
        for task in data['tasks']:
            db.execute('''
                INSERT OR REPLACE INTO tasks (
                    id, name, description, start_time, end_time,
                    status, priority, tags, location, completion_count,
                    required_count, estimated_duration, commute_time,
                    rest_time, period_type, period_value,
                    completion_times_type, completion_times_value,
                    time_slot_start, time_slot_end, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task['id'],
                task['name'],
                task.get('description', ''),
                task['start_time'],
                task.get('end_time'),
                task['status'],
                task['priority'],
                json.dumps(task.get('tags', []), ensure_ascii=False),
                task.get('location'),
                task.get('completion_count', 0),
                task.get('required_count'),
                task.get('estimated_duration'),
                task.get('commute_time'),
                task.get('rest_time'),
                task.get('period_type'),
                task.get('period_value'),
                task.get('completion_times_type'),
                task.get('completion_times_value'),
                task.get('time_slot_start'),
                task.get('time_slot_end'),
                task['created_at'],
                now
            ))
    else:
        # 从服务器下载数据
        tasks = db.execute('SELECT * FROM tasks').fetchall()
        return jsonify({
            'code': 200,
            'data': {
                'tasks': [dict(task) for task in tasks]
            },
            'message': '同步任务成功'
        })
    
    db.commit()
    return jsonify({
        'code': 200,
        'message': '同步任务成功'
    })

@bp.route('/status', methods=['GET'])
def get_sync_status():
    """获取同步状态"""
    status = sync_service.get_status()
    return jsonify({
        'success': True,
        'data': status
    }) 