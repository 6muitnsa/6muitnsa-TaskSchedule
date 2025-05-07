from flask import Blueprint, request, jsonify
from services.notification_service import NotificationService
from models.notification import NotificationCreate, NotificationUpdate

bp = Blueprint('notifications', __name__)
notification_service = NotificationService()

@bp.route('/', methods=['GET'])
def get_notifications():
    """获取所有通知"""
    task_id = request.args.get('task_id', type=int)
    notifications = notification_service.get_notifications(task_id)
    return jsonify([notification.model_dump() for notification in notifications])

@bp.route('/', methods=['POST'])
def create_notification():
    """创建通知"""
    data = request.get_json()
    notification = NotificationCreate(**data)
    created_notification = notification_service.create_notification(notification)
    return jsonify(created_notification.model_dump()), 201

@bp.route('/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    """获取单个通知"""
    notification = notification_service.get_notification(notification_id)
    if notification:
        return jsonify(notification.model_dump())
    return jsonify({'error': 'Notification not found'}), 404

@bp.route('/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    """更新通知"""
    data = request.get_json()
    notification = NotificationUpdate(**data)
    updated_notification = notification_service.update_notification(notification_id, notification)
    if updated_notification:
        return jsonify(updated_notification.model_dump())
    return jsonify({'error': 'Notification not found'}), 404

@bp.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """删除通知"""
    if notification_service.delete_notification(notification_id):
        return '', 204
    return jsonify({'error': 'Notification not found'}), 404

@bp.route('/<int:notification_id>/read', methods=['POST'])
def mark_as_read(notification_id):
    """标记通知为已读"""
    notification = notification_service.mark_as_read(notification_id)
    if notification:
        return jsonify(notification.model_dump())
    return jsonify({'error': 'Notification not found'}), 404 