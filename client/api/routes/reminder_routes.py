from flask import Blueprint, request, jsonify
from services.reminder_service import ReminderService
from models.reminder import ReminderCreate, ReminderUpdate

bp = Blueprint('reminders', __name__)
reminder_service = ReminderService()

@bp.route('/', methods=['GET'])
def get_reminders():
    """获取所有提醒"""
    task_id = request.args.get('task_id', type=int)
    reminders = reminder_service.get_reminders(task_id)
    return jsonify([reminder.model_dump() for reminder in reminders])

@bp.route('/', methods=['POST'])
def create_reminder():
    """创建提醒"""
    data = request.get_json()
    reminder = ReminderCreate(**data)
    created_reminder = reminder_service.create_reminder(reminder)
    return jsonify(created_reminder.model_dump()), 201

@bp.route('/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    """获取单个提醒"""
    reminder = reminder_service.get_reminder(reminder_id)
    if reminder:
        return jsonify(reminder.model_dump())
    return jsonify({'error': 'Reminder not found'}), 404

@bp.route('/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    """更新提醒"""
    data = request.get_json()
    reminder = ReminderUpdate(**data)
    updated_reminder = reminder_service.update_reminder(reminder_id, reminder)
    if updated_reminder:
        return jsonify(updated_reminder.model_dump())
    return jsonify({'error': 'Reminder not found'}), 404

@bp.route('/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    """删除提醒"""
    if reminder_service.delete_reminder(reminder_id):
        return '', 204
    return jsonify({'error': 'Reminder not found'}), 404

@bp.route('/check', methods=['POST'])
def check_reminders():
    """检查并触发提醒"""
    reminder_service.check_reminders()
    return jsonify({'message': 'Reminders checked'}) 