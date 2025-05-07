from flask import Blueprint, request, jsonify
from database import get_db
import json
from services.settings_service import SettingsService
import os
import traceback

bp = Blueprint('settings', __name__)
settings_service = SettingsService()

@bp.route('/', methods=['GET'])
def get_settings():
    """获取所有设置"""
    settings = settings_service.get_all_settings()
    return jsonify({
        'code': 200,
        'data': settings,
        'message': '获取设置成功'
    })

@bp.route('/', methods=['PUT'])
def update_settings():
    """更新设置"""
    try:
        print("收到更新设置请求")
        print("请求方法:", request.method)
        print("请求路径:", request.path)
        print("请求头:", dict(request.headers))
        
        data = request.get_json()
        print("请求数据:", data)
        
        updated_settings = settings_service.update_settings(data)
        print("更新后的设置:", updated_settings)
        
        return jsonify({
            'code': 200,
            'data': updated_settings,
            'message': '更新设置成功'
        })
    except Exception as e:
        print("更新设置失败:", str(e))
        print("错误详情:", {
            'type': type(e).__name__,
            'message': str(e),
            'traceback': traceback.format_exc()
        })
        return jsonify({
            'code': 500,
            'message': f'更新设置失败: {str(e)}'
        }), 500

@bp.route('/scheduler', methods=['GET'])
def get_scheduler_settings():
    """获取调度设置"""
    settings = settings_service.get_setting('scheduler', {})
    return jsonify({
        'code': 200,
        'data': settings,
        'message': '获取调度设置成功'
    })

@bp.route('/scheduler', methods=['PUT'])
def update_scheduler_settings():
    """更新调度设置"""
    try:
        data = request.get_json()
        settings_service.update_setting('scheduler', data)
        return jsonify({
            'code': 200,
            'data': data,
            'message': '更新调度设置成功'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新调度设置失败: {str(e)}'
        }), 500

@bp.route('/priority', methods=['GET'])
def get_priority_settings():
    db = get_db()
    settings = db.execute('''
        SELECT key, value FROM settings
        WHERE category = 'priority'
    ''').fetchall()
    
    result = {}
    for setting in settings:
        result[setting['key']] = json.loads(setting['value'])
    
    return jsonify({
        'code': 200,
        'data': result,
        'message': '获取优先级设置成功'
    })

@bp.route('/priority', methods=['PUT'])
def update_priority_settings():
    data = request.get_json()
    db = get_db()
    
    for key, value in data.items():
        db.execute('''
            INSERT OR REPLACE INTO settings (category, key, value)
            VALUES ('priority', ?, ?)
        ''', (key, json.dumps(value)))
    
    db.commit()
    return jsonify({
        'code': 200,
        'data': {
            'status': 'success'
        },
        'message': '更新优先级设置成功'
    })

@bp.route('/time-prediction', methods=['GET'])
def get_time_prediction_settings():
    db = get_db()
    settings = db.execute('''
        SELECT key, value FROM settings
        WHERE category = 'time_prediction'
    ''').fetchall()
    
    result = {}
    for setting in settings:
        result[setting['key']] = json.loads(setting['value'])
    
    return jsonify({
        'code': 200,
        'data': result,
        'message': '获取时间预测设置成功'
    })

@bp.route('/time-prediction', methods=['PUT'])
def update_time_prediction_settings():
    data = request.get_json()
    db = get_db()
    
    for key, value in data.items():
        db.execute('''
            INSERT OR REPLACE INTO settings (category, key, value)
            VALUES ('time_prediction', ?, ?)
        ''', (key, json.dumps(value)))
    
    db.commit()
    return jsonify({
        'code': 200,
        'data': {
            'status': 'success'
        },
        'message': '更新时间预测设置成功'
    })

@bp.route('/path', methods=['GET'])
def get_path_settings():
    """获取路径设置"""
    path = settings_service.get_path()
    return jsonify({
        'code': 200,
        'data': path,
        'message': '获取路径设置成功'
    })

@bp.route('/path', methods=['PUT'])
def update_path_settings():
    """更新路径设置"""
    try:
        data = request.get_json()
        updated_paths = settings_service.update_path(data)
        return jsonify({
            'code': 200,
            'data': updated_paths,
            'message': '更新路径设置成功'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新路径设置失败: {str(e)}'
        }), 500

@bp.route('/settings/path', methods=['GET'])
def get_path():
    """获取路径设置"""
    path = settings_service.get_path()
    return jsonify({
        'success': True,
        'data': path
    })

@bp.route('/path', methods=['GET'])
def get_config_path():
    """获取配置文件路径"""
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.json')
        return jsonify({
            'code': 200,
            'data': config_path,
            'message': '获取配置文件路径成功'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取配置文件路径失败: {str(e)}'
        }), 500

@bp.route('/load', methods=['POST'])
def load_settings():
    """加载设置"""
    try:
        data = request.get_json()
        path = data.get('path')
        
        if not path or not os.path.exists(path):
            return jsonify({
                'code': 400,
                'message': '配置文件路径无效'
            }), 400
        
        with open(path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        return jsonify({
            'code': 200,
            'data': settings,
            'message': '加载设置成功'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'加载设置失败: {str(e)}'
        }), 500 