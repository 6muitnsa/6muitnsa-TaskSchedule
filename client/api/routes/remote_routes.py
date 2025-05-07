import os
import time
import tempfile
import subprocess
from pathlib import Path
from flask import Blueprint, jsonify, request
from utils.cloudflared import CloudflaredManager
import qrcode
import io
import base64
import yaml

# 读取配置文件
config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

bp = Blueprint('remote', __name__, url_prefix='/api/remote')
sync_bp = Blueprint('remote_sync', __name__, url_prefix='/api/sync')

# 创建 CloudflaredManager 实例
cloudflared_manager = CloudflaredManager()

def generate_qrcode(url):
    """生成二维码"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # 创建二维码图片
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 转换为base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@bp.route('/start', methods=['POST'])
def start_remote():
    """启动远程访问服务"""
    try:
        # 启动 cloudflared 并获取 URL
        url = cloudflared_manager.start_tunnel('remote', config['frontend']['port'])  # 使用配置的前端端口
        qrcode = generate_qrcode(url)
        return jsonify({
            'status': 'success',
            'url': url,
            'qrcode': qrcode
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/stop', methods=['POST'])
def stop_remote():
    """停止远程访问服务"""
    try:
        cloudflared_manager.stop_tunnel('remote')
        return jsonify({
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@sync_bp.route('/start', methods=['POST'])
def start_sync():
    """启动数据同步服务"""
    try:
        # 启动 cloudflared 并获取 URL
        url = cloudflared_manager.start_tunnel('sync', config['app']['port'])  # 使用配置的后端端口
        qrcode = generate_qrcode(url)
        return jsonify({
            'status': 'success',
            'url': url,
            'qrcode': qrcode
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@sync_bp.route('/confirm', methods=['POST'])
def confirm_sync():
    """确认数据同步"""
    try:
        direction = request.json.get('direction', 'client')
        # TODO: 实现数据同步逻辑
        return jsonify({
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@sync_bp.route('/stop', methods=['POST'])
def stop_sync():
    """停止数据同步服务"""
    try:
        cloudflared_manager.stop_tunnel('sync')
        return jsonify({
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 