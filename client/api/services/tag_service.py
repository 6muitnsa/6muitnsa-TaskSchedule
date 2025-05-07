from datetime import datetime
from typing import List, Optional
from models.tag import Tag, TagCreate, TagUpdate
from database import get_db

class TagService:
    def __init__(self):
        pass

    def get_all_tags(self):
        """获取所有标签"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tags ORDER BY created_at DESC')
        tags = cursor.fetchall()
        db.close()
        return [dict(tag) for tag in tags]

    def create_tag(self, name, color):
        """创建新标签"""
        db = get_db()
        cursor = db.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO tags (name, color, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (name, color, now, now))
        
        tag_id = cursor.lastrowid
        db.commit()
        db.close()
        
        return {
            'id': tag_id,
            'name': name,
            'color': color,
            'created_at': now,
            'updated_at': now
        }

    def update_tag(self, tag_id, name, color):
        """更新标签"""
        db = get_db()
        cursor = db.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE tags 
            SET name = ?, color = ?, updated_at = ?
            WHERE id = ?
        ''', (name, color, now, tag_id))
        
        success = cursor.rowcount > 0
        db.commit()
        db.close()
        return success

    def delete_tag(self, tag_id):
        """删除标签"""
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
        
        success = cursor.rowcount > 0
        db.commit()
        db.close()
        return success

    def add_tag(self, tag: TagCreate) -> Tag:
        """添加标签"""
        now = datetime.now()
        tag_dict = tag.model_dump()
        tag_dict.update({
            'created_at': now,
            'updated_at': now
        })
        
        cursor = get_db().cursor()
        cursor.execute("""
            INSERT INTO tags (name, color, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (
            tag_dict['name'],
            tag_dict['color'],
            tag_dict['created_at'],
            tag_dict['updated_at']
        ))
        get_db().commit()
        
        tag_dict['id'] = cursor.lastrowid
        return Tag(**tag_dict)

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        """获取单个标签"""
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM tags WHERE id = ?", (tag_id,))
        tag = cursor.fetchone()
        return Tag(**dict(tag)) if tag else None 