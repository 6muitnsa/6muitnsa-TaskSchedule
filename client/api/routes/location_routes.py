from flask import Blueprint, request, jsonify
from services.location_service import LocationService
from models.location import LocationCreate, LocationUpdate

bp = Blueprint('locations', __name__)
location_service = LocationService()

@bp.route('/', methods=['GET'])
def get_locations():
    """获取所有位置"""
    locations = location_service.get_locations()
    return jsonify([location.model_dump() for location in locations])

@bp.route('/', methods=['POST'])
def create_location():
    """创建位置"""
    data = request.get_json()
    location = LocationCreate(**data)
    created_location = location_service.add_location(location)
    return jsonify(created_location.model_dump()), 201

@bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """获取单个位置"""
    location = location_service.get_location(location_id)
    if location:
        return jsonify(location.model_dump())
    return jsonify({'error': 'Location not found'}), 404

@bp.route('/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """删除位置"""
    if location_service.delete_location(location_id):
        return '', 204
    return jsonify({'error': 'Location not found'}), 404 