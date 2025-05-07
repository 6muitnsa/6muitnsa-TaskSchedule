import qrcode
import json
import base64
from io import BytesIO
from datetime import datetime
from typing import Optional, Dict, Any
from models.sync_record import SyncRecord, SyncRecordCreate
from database import get_db

class SyncService:
    def __init__(self):
        pass

    def generate_qr_code(self, device_id: str) -> str:
        """生成同步二维码"""
        # 创建同步数据
        sync_data = {
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }
        
        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(sync_data))
        qr.make(fit=True)
        
        # 转换为base64图片
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

    def sync_data(self, device_id: str, data: Dict[str, Any]) -> SyncRecord:
        """同步数据"""
        # 创建同步记录
        sync_record = SyncRecordCreate(
            device_id=device_id,
            sync_time=datetime.now(),
            status='success',
            details=json.dumps(data)
        )
        
        # 保存同步记录
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO sync_records (device_id, sync_time, status, details, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            sync_record.device_id,
            sync_record.sync_time,
            sync_record.status,
            sync_record.details,
            datetime.now(),
            datetime.now()
        ))
        db.commit()
        
        # 返回同步记录
        sync_record_dict = sync_record.model_dump()
        sync_record_dict['id'] = cursor.lastrowid
        return SyncRecord(**sync_record_dict)

    def get_status(self):
        """获取同步状态"""
        now = datetime.now()
        db = get_db()
        
        # 获取最近的同步记录
        last_sync = db.execute('''
            SELECT * FROM sync_records
            ORDER BY sync_time DESC
            LIMIT 1
        ''').fetchone()
        
        if not last_sync:
            return {
                'lastSyncTime': None,
                'status': 'never',
                'direction': None,
                'syncId': None
            }
        
        # 计算同步状态
        sync_time = datetime.fromisoformat(last_sync['sync_time'])
        time_diff = (now - sync_time).total_seconds()
        
        if time_diff < 300:  # 5分钟内
            status = 'success'
        elif time_diff < 3600:  # 1小时内
            status = 'warning'
        else:
            status = 'error'
        
        return {
            'lastSyncTime': last_sync['sync_time'],
            'status': status,
            'direction': last_sync.get('direction'),
            'syncId': last_sync.get('sync_id')
        }

    def get_sync_history(self, device_id: str) -> list[SyncRecord]:
        """获取同步历史"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM sync_records 
            WHERE device_id = ? 
            ORDER BY sync_time DESC
        """, (device_id,))
        records = cursor.fetchall()
        return [SyncRecord(**dict(record)) for record in records] 