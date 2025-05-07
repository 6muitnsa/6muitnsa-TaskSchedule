from flask import Blueprint, request, jsonify
from services.location_service import LocationService
from models.location import LocationCreate, LocationUpdate
import logging

bp = Blueprint('locations', __name__)
location_service = LocationService()
logger = logging.getLogger(__name__)

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

@bp.route('/routes', methods=['GET'])
def get_location_routes():
    """获取所有地点路由"""
    logger.info("获取所有地点路由")
    routes = location_service.get_location_routes()
    logger.info(f"获取到 {len(routes)} 条路由")
    return jsonify(routes)

@bp.route('/routes', methods=['POST'])
def create_location_route():
    """创建地点路由"""
    data = request.get_json()
    logger.info(f"创建地点路由: {data}")
    try:
        route = location_service.add_location_route(data)
        logger.info(f"地点路由创建成功: {route}")
        return jsonify(route), 201
    except Exception as e:
        logger.error(f"创建地点路由失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@bp.route('/routes/<int:route_id>', methods=['DELETE'])
def delete_location_route(route_id):
    """删除地点路由"""
    logger.info(f"删除地点路由: {route_id}")
    if location_service.delete_location_route(route_id):
        logger.info(f"地点路由删除成功: {route_id}")
        return '', 204
    logger.warning(f"地点路由不存在: {route_id}")
    return jsonify({'error': 'Route not found'}), 404 