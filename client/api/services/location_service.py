from datetime import datetime
from typing import List, Optional
from models.location import Location, LocationCreate, LocationUpdate
from database import get_db

class LocationService:
    def __init__(self):
        self.db = get_db()

    def add_location(self, location: LocationCreate) -> Location:
        """添加位置"""
        now = datetime.now()
        location_dict = location.model_dump()
        location_dict.update({
            'created_at': now,
            'updated_at': now
        })
        
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO locations (name, address, latitude, longitude, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            location_dict['name'],
            location_dict['address'],
            location_dict['latitude'],
            location_dict['longitude'],
            location_dict['created_at'],
            location_dict['updated_at']
        ))
        self.db.commit()
        
        location_dict['id'] = cursor.lastrowid
        return Location(**location_dict)

    def get_locations(self) -> List[Location]:
        """获取所有位置"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM locations ORDER BY created_at DESC")
        locations = cursor.fetchall()
        return [Location(**dict(location)) for location in locations]

    def get_location(self, location_id: int) -> Optional[Location]:
        """获取单个位置"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM locations WHERE id = ?", (location_id,))
        location = cursor.fetchone()
        return Location(**dict(location)) if location else None

    def update_location(self, location_id: int, location: LocationUpdate) -> Optional[Location]:
        """更新位置"""
        cursor = self.db.cursor()
        updates = []
        values = []
        
        for field, value in location.model_dump(exclude_unset=True).items():
            if value is not None:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return self.get_location(location_id)
        
        values.append(datetime.now())  # updated_at
        values.append(location_id)
        
        query = f"""
            UPDATE locations 
            SET {', '.join(updates)}, updated_at = ?
            WHERE id = ?
        """
        
        cursor.execute(query, values)
        self.db.commit()
        
        return self.get_location(location_id)

    def delete_location(self, location_id: int) -> bool:
        """删除位置"""
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM locations WHERE id = ?", (location_id,))
        self.db.commit()
        return cursor.rowcount > 0 