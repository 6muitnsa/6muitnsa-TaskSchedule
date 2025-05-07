from datetime import datetime
from typing import List, Optional, Dict
from models.location import Location, LocationCreate, LocationUpdate
from database import get_db
import logging

logger = logging.getLogger(__name__)

class LocationService:
    def add_location(self, location: LocationCreate) -> Location:
        """添加位置"""
        now = datetime.now()
        location_dict = location.model_dump()
        location_dict.update({
            'created_at': now,
            'updated_at': now
        })
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO locations (name, created_at, updated_at)
            VALUES (?, ?, ?)
        """, (
            location_dict['name'],
            location_dict['created_at'],
            location_dict['updated_at']
        ))
        db.commit()
        
        location_dict['id'] = cursor.lastrowid
        return Location(**location_dict)

    def get_locations(self) -> List[Location]:
        """获取所有位置"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM locations ORDER BY created_at DESC")
        locations = cursor.fetchall()
        return [Location(**dict(location)) for location in locations]

    def get_location(self, location_id: int) -> Optional[Location]:
        """获取单个位置"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM locations WHERE id = ?", (location_id,))
        location = cursor.fetchone()
        return Location(**dict(location)) if location else None

    def update_location(self, location_id: int, location: LocationUpdate) -> Optional[Location]:
        """更新位置"""
        db = get_db()
        cursor = db.cursor()
        now = datetime.now()
        
        cursor.execute("""
            UPDATE locations 
            SET name = ?, updated_at = ?
            WHERE id = ?
        """, (location.name, now, location_id))
        
        db.commit()
        return self.get_location(location_id)

    def delete_location(self, location_id: int) -> bool:
        """删除位置"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM locations WHERE id = ?", (location_id,))
        db.commit()
        return cursor.rowcount > 0

    def get_location_routes(self) -> List[Dict]:
        """获取所有地点路由"""
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""
                SELECT lr.*, l1.name as from_name, l2.name as to_name
                FROM location_routes lr
                JOIN locations l1 ON lr.from_location_id = l1.id
                JOIN locations l2 ON lr.to_location_id = l2.id
                ORDER BY lr.created_at DESC
            """)
            routes = cursor.fetchall()
            logger.info(f"从数据库获取到 {len(routes)} 条路由记录")
            return [dict(route) for route in routes]
        except Exception as e:
            logger.error(f"获取地点路由失败: {str(e)}")
            raise

    def add_location_route(self, data: Dict) -> Dict:
        """添加地点路由"""
        try:
            db = get_db()
            cursor = db.cursor()
            now = datetime.now()

            # 获取地点ID
            cursor.execute("SELECT id FROM locations WHERE name = ?", (data['from'],))
            from_location = cursor.fetchone()
            if not from_location:
                logger.error(f"起点不存在: {data['from']}")
                raise ValueError(f"起点不存在: {data['from']}")

            cursor.execute("SELECT id FROM locations WHERE name = ?", (data['to'],))
            to_location = cursor.fetchone()
            if not to_location:
                logger.error(f"终点不存在: {data['to']}")
                raise ValueError(f"终点不存在: {data['to']}")

            # 检查是否已存在相同的路由
            cursor.execute("""
                SELECT id FROM location_routes 
                WHERE from_location_id = ? AND to_location_id = ?
            """, (from_location['id'], to_location['id']))
            existing_route = cursor.fetchone()
            if existing_route:
                logger.error(f"路由已存在: {data['from']} -> {data['to']}")
                raise ValueError(f"路由已存在: {data['from']} -> {data['to']}")

            # 插入路由
            cursor.execute("""
                INSERT INTO location_routes (
                    from_location_id, to_location_id, commute_time,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                from_location['id'],
                to_location['id'],
                data['time'],
                now,
                now
            ))
            db.commit()
            logger.info(f"成功添加路由: {data['from']} -> {data['to']}")

            # 获取插入的路由信息
            route_id = cursor.lastrowid
            cursor.execute("""
                SELECT lr.*, l1.name as from_name, l2.name as to_name
                FROM location_routes lr
                JOIN locations l1 ON lr.from_location_id = l1.id
                JOIN locations l2 ON lr.to_location_id = l2.id
                WHERE lr.id = ?
            """, (route_id,))
            route = cursor.fetchone()
            return dict(route)
        except Exception as e:
            logger.error(f"添加地点路由失败: {str(e)}")
            raise

    def delete_location_route(self, route_id: int) -> bool:
        """删除地点路由"""
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM location_routes WHERE id = ?", (route_id,))
            db.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"成功删除路由: {route_id}")
            else:
                logger.warning(f"路由不存在: {route_id}")
            return success
        except Exception as e:
            logger.error(f"删除地点路由失败: {str(e)}")
            raise 