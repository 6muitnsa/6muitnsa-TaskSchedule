from flask import Blueprint, request, jsonify
from services.tag_service import TagService
from datetime import datetime

bp = Blueprint('tag', __name__)
tag_service = TagService()

@bp.route('/', methods=['GET'])
def get_tags():
    """获取所有标签"""
    tags = tag_service.get_all_tags()
    return jsonify({
        'success': True,
        'data': tags
    })

@bp.route('/', methods=['POST'])
def create_tag():
    """创建新标签"""
    data = request.get_json()
    name = data.get('name')
    color = data.get('color')
    
    if not name or not color:
        return jsonify({
            'success': False,
            'message': '标签名称和颜色不能为空'
        }), 400
    
    tag = tag_service.create_tag(name, color)
    return jsonify({
        'success': True,
        'data': tag
    })

@bp.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    """更新标签"""
    data = request.get_json()
    name = data.get('name')
    color = data.get('color')
    
    if not name or not color:
        return jsonify({
            'success': False,
            'message': '标签名称和颜色不能为空'
        }), 400
    
    success = tag_service.update_tag(tag_id, name, color)
    if success:
        return jsonify({
            'success': True,
            'message': '标签更新成功'
        })
    return jsonify({
        'success': False,
        'message': '标签不存在'
    }), 404

@bp.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """删除标签"""
    success = tag_service.delete_tag(tag_id)
    if success:
        return jsonify({
            'success': True,
            'message': '标签删除成功'
        })
    return jsonify({
        'success': False,
        'message': '标签不存在'
    }), 404 