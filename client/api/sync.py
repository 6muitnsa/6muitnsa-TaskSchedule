from flask import Blueprint, jsonify
from ..util.sync import sync_manager

bp = Blueprint('sync', __name__)

@bp.route('/sync/start', methods=['POST'])
def start_sync():
    """启动同步服务"""
    try:
        url, qrcode = sync_manager.start()
        return jsonify({
            'success': True,
            'url': url,
            'qrcode': qrcode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/sync/stop', methods=['POST'])
def stop_sync():
    """停止同步服务"""
    try:
        sync_manager.stop()
        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/sync/status', methods=['GET'])
def get_sync_status():
    """获取同步状态"""
    try:
        is_running, url, qrcode = sync_manager.get_status()
        return jsonify({
            'success': True,
            'isRunning': is_running,
            'url': url,
            'qrcode': qrcode
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500 