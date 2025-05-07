from database import get_db

def init_data():
    """初始化示例数据"""
    db = get_db()
    cursor = db.cursor()
    
    # 插入标签数据
    cursor.executemany(
        'INSERT INTO tags (name, color, created_at, updated_at) VALUES (?, ?, datetime("now"), datetime("now"))',
        [
            ('工作', '#FF0000'),
            ('学习', '#00FF00'),
            ('生活', '#0000FF')
        ]
    )
    
    # 插入位置数据
    cursor.executemany(
        'INSERT INTO locations (name, created_at, updated_at) VALUES (?, datetime("now"), datetime("now"))',
        [
            ('公司',),
            ('家',),
            ('图书馆',)
        ]
    )
    
    # 插入任务数据
    cursor.executemany(
        '''INSERT INTO tasks 
           (title, description, priority, status, due_date, location, estimated_time, tags, created_at, updated_at) 
           VALUES (?, ?, ?, ?, datetime('now', ?), ?, ?, ?, datetime('now'), datetime('now'))''',
        [
            ('完成项目报告', '编写项目进度报告并提交', 3000, 'pending', '+2 days', '公司', 120, '工作'),
            ('学习Vue.js', '完成Vue.js基础教程', 2000, 'pending', '+5 days', '图书馆', 180, '学习'),
            ('购物清单', '购买生活必需品', 1000, 'pending', '+1 day', '家', 60, '生活')
        ]
    )
    
    # 插入任务标签关联
    cursor.executemany(
        'INSERT INTO task_tags (task_id, tag_id, created_at) VALUES (?, ?, datetime("now"))',
        [
            (1, 1),  # 工作标签
            (2, 2),  # 学习标签
            (3, 3)   # 生活标签
        ]
    )
    
    # 插入位置路由
    cursor.executemany(
        'INSERT INTO location_routes (from_location_id, to_location_id, commute_time, created_at, updated_at) VALUES (?, ?, ?, datetime("now"), datetime("now"))',
        [
            (1, 2, 30),  # 公司到家
            (2, 3, 20),  # 家到图书馆
            (3, 1, 40)   # 图书馆到公司
        ]
    )
    
    # 插入任务位置关联
    cursor.executemany(
        'INSERT INTO task_locations (task_id, location_id, created_at) VALUES (?, ?, datetime("now"))',
        [
            (1, 1),  # 任务1在公司
            (2, 3),  # 任务2在图书馆
            (3, 2)   # 任务3在家
        ]
    )
    
    # 插入提醒
    cursor.executemany(
        "INSERT INTO reminders (task_id, time, type, status, created_at) VALUES (?, datetime('now', ?), ?, 'pending', datetime('now'))",
        [
            (1, '+1 day', 'email'),
            (2, '+4 days', 'notification'),
            (3, '+12 hours', 'sms')
        ]
    )
    
    # 插入通知
    cursor.executemany(
        'INSERT INTO notifications (task_id, type, message, status, created_at) VALUES (?, ?, ?, "unread", datetime("now"))',
        [
            (1, 'reminder', '项目报告即将到期'),
            (2, 'update', 'Vue.js教程已更新'),
            (3, 'reminder', '购物清单待完成')
        ]
    )
    
    # 插入同步记录
    cursor.executemany(
        'INSERT INTO sync_records (device_id, status, sync_time) VALUES (?, ?, datetime("now"))',
        [
            ('device1', 'success'),
            ('device2', 'success'),
            ('device3', 'success')
        ]
    )
    
    # 插入番茄钟记录
    cursor.executemany(
        "INSERT INTO pomodoro_records (task_id, start_time, duration, status, created_at) VALUES (?, datetime('now', ?), ?, ?, datetime('now'))",
        [
            (1, '-2 hours', 25, 'completed'),
            (2, '-1 hour', 25, 'completed'),
            (3, '0 hours', 25, 'in_progress')
        ]
    )
    
    db.commit()
    print("示例数据初始化完成")

if __name__ == '__main__':
    init_data() 