from flask import Blueprint, jsonify
from services.scheduler_service import SchedulerService

bp = Blueprint('scheduler', __name__)
scheduler_service = SchedulerService()

@bp.route('/status', methods=['GET'])
def get_status():
    """获取调度器状态"""
    status = scheduler_service.get_status()
    return jsonify({
        'success': True,
        'data': status
    })

@bp.route('/results', methods=['GET'])
def get_results():
    """获取调度结果"""
    results = scheduler_service.get_results()
    return jsonify({
        'success': True,
        'data': results
    }) 