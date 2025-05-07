from flask import Blueprint, jsonify
from services.scheduler_service import SchedulerService
from utils.response import success_response, error_response

bp = Blueprint('scheduler', __name__)
scheduler_service = SchedulerService()

@bp.route('/status', methods=['GET'])
def get_status():
    """获取调度器状态"""
    try:
        status = scheduler_service.get_status()
        return success_response(data=status, message='获取调度器状态成功')
    except Exception as e:
        return error_response(message=f'获取调度器状态失败: {str(e)}')

@bp.route('/results', methods=['GET'])
def get_results():
    """获取调度结果"""
    try:
        results = scheduler_service.get_results()
        return success_response(data=results, message='获取调度结果成功')
    except Exception as e:
        return error_response(message=f'获取调度结果失败: {str(e)}')

@bp.route('/schedule', methods=['POST'])
def schedule():
    """触发调度"""
    try:
        results = scheduler_service.schedule_tasks()
        return success_response(data=results, message='调度任务成功')
    except Exception as e:
        return error_response(message=f'调度任务失败: {str(e)}') 