from database import get_db
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config import Config

class SchedulerService:
    def __init__(self):
        self._init_table()
        self.config = Config()

    def _init_table(self):
        """初始化调度结果表"""
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS scheduler_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        db.commit()

    def get_status(self):
        """获取调度器状态"""
        db = get_db()
        last_result = db.execute('''
            SELECT created_at, algorithm FROM scheduler_results
            ORDER BY created_at DESC
            LIMIT 1
        ''').fetchone()
        
        return {
            'is_running': False,
            'last_run': last_result['created_at'] if last_result else None,
            'last_algorithm': last_result['algorithm'] if last_result else None,
            'next_run': (datetime.now() + timedelta(hours=1)).isoformat() if last_result else None
        }

    def get_results(self):
        """获取调度结果"""
        try:
            db = get_db()
            results = db.execute('''
                SELECT sr.*, t.title as task_title, t.priority, t.estimated_duration
                FROM scheduler_results sr
                LEFT JOIN tasks t ON sr.task_id = t.id
                ORDER BY sr.created_at DESC
                LIMIT 100
            ''').fetchall()
            return [dict(result) for result in results]
        except Exception as e:
            print(f"获取调度结果失败: {str(e)}")
            return []

    def _fcfs_schedule(self, tasks: List[Dict]) -> List[Dict]:
        """先来先服务调度算法"""
        # 按创建时间排序
        sorted_tasks = sorted(tasks, key=lambda x: x['created_at'])
        
        # 计算每个任务的开始和结束时间
        current_time = datetime.now()
        scheduled_tasks = []
        
        for task in sorted_tasks:
            # 如果任务有固定时间段，则使用固定时间段
            if task.get('time_slot_start') and task.get('time_slot_end'):
                continue
                
            # 计算任务实际开始时间（考虑通勤时间）
            commute_time = task.get('commute_time', 0)
            start_time = current_time + timedelta(minutes=commute_time)
            
            # 计算任务结束时间（考虑休息时间）
            duration = task.get('estimated_duration', 30)
            rest_time = task.get('rest_time', 5)
            end_time = start_time + timedelta(minutes=duration + rest_time)
            
            scheduled_tasks.append({
                'task_id': task['id'],
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'status': 'scheduled'
            })
            
            # 更新当前时间
            current_time = end_time
        
        return scheduled_tasks

    def _sjf_schedule(self, tasks: List[Dict]) -> List[Dict]:
        """短作业优先调度算法"""
        # 过滤出没有固定时间段的任务
        flexible_tasks = [t for t in tasks if not (t.get('time_slot_start') and t.get('time_slot_end'))]
        fixed_tasks = [t for t in tasks if t.get('time_slot_start') and t.get('time_slot_end')]
        
        # 按预计完成时间排序
        sorted_tasks = sorted(flexible_tasks, key=lambda x: x.get('estimated_duration', 30))
        
        # 计算每个任务的开始和结束时间
        current_time = datetime.now()
        scheduled_tasks = []
        
        for task in sorted_tasks:
            # 计算任务实际开始时间（考虑通勤时间）
            commute_time = task.get('commute_time', 0)
            start_time = current_time + timedelta(minutes=commute_time)
            
            # 计算任务结束时间（考虑休息时间）
            duration = task.get('estimated_duration', 30)
            rest_time = task.get('rest_time', 5)
            end_time = start_time + timedelta(minutes=duration + rest_time)
            
            scheduled_tasks.append({
                'task_id': task['id'],
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'status': 'scheduled'
            })
            
            # 更新当前时间
            current_time = end_time
        
        return scheduled_tasks

    def _rr_schedule(self, tasks: List[Dict], time_slice: int = 25) -> List[Dict]:
        """轮转调度算法"""
        # 过滤出没有固定时间段的任务
        flexible_tasks = [t for t in tasks if not (t.get('time_slot_start') and t.get('time_slot_end'))]
        fixed_tasks = [t for t in tasks if t.get('time_slot_start') and t.get('time_slot_end')]
        
        # 初始化任务剩余时间
        for task in flexible_tasks:
            task['remaining_time'] = task.get('estimated_duration', 30)
            task['slices'] = []
        
        current_time = datetime.now()
        scheduled_tasks = []
        
        while any(task['remaining_time'] > 0 for task in flexible_tasks):
            for task in flexible_tasks:
                if task['remaining_time'] <= 0:
                    continue
                    
                # 计算本次时间片
                slice_duration = min(time_slice, task['remaining_time'])
                
                # 记录时间片
                slice_start = current_time
                slice_end = slice_start + timedelta(minutes=slice_duration)
                task['slices'].append({
                    'start': slice_start,
                    'end': slice_end
                })
                
                # 更新任务剩余时间
                task['remaining_time'] -= slice_duration
                
                # 更新当前时间（考虑休息时间）
                rest_time = task.get('rest_time', 5)
                current_time = slice_end + timedelta(minutes=rest_time)
        
        # 计算每个任务的最终开始和结束时间
        for task in flexible_tasks:
            if task['slices']:
                scheduled_tasks.append({
                    'task_id': task['id'],
                    'start_time': task['slices'][0]['start'].isoformat(),
                    'end_time': task['slices'][-1]['end'].isoformat(),
                    'status': 'scheduled'
                })
        
        return scheduled_tasks

    def _priority_schedule(self, tasks: List[Dict]) -> List[Dict]:
        """优先级调度算法"""
        # 过滤出没有固定时间段的任务
        flexible_tasks = [t for t in tasks if not (t.get('time_slot_start') and t.get('time_slot_end'))]
        fixed_tasks = [t for t in tasks if t.get('time_slot_start') and t.get('time_slot_end')]
        
        # 按优先级排序（优先级数值越大，优先级越高）
        sorted_tasks = sorted(flexible_tasks, key=lambda x: x.get('priority', 0), reverse=True)
        
        # 计算每个任务的开始和结束时间
        current_time = datetime.now()
        scheduled_tasks = []
        
        for task in sorted_tasks:
            # 计算任务实际开始时间（考虑通勤时间）
            commute_time = task.get('commute_time', 0)
            start_time = current_time + timedelta(minutes=commute_time)
            
            # 计算任务结束时间（考虑休息时间）
            duration = task.get('estimated_duration', 30)
            rest_time = task.get('rest_time', 5)
            end_time = start_time + timedelta(minutes=duration + rest_time)
            
            scheduled_tasks.append({
                'task_id': task['id'],
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'status': 'scheduled'
            })
            
            # 更新当前时间
            current_time = end_time
        
        return scheduled_tasks

    def schedule_tasks(self, algorithm: str = None):
        """调度任务"""
        try:
            db = get_db()
            now = datetime.now()
            
            # 获取待调度的任务
            tasks = db.execute('''
                SELECT * FROM tasks
                WHERE status = 'pending'
                AND (due_date IS NULL OR due_date > ?)
            ''', (now.isoformat(),)).fetchall()
            
            # 如果没有指定算法，使用配置中的默认算法
            if not algorithm:
                algorithm = self.config.get_setting('scheduler', {}).get('default_algorithm', 'priority')
            
            # 选择调度算法
            schedulers = {
                'fcfs': self._fcfs_schedule,
                'sjf': self._sjf_schedule,
                'rr': self._rr_schedule,
                'priority': self._priority_schedule
            }
            
            if algorithm not in schedulers:
                raise ValueError(f"不支持的调度算法: {algorithm}")
            
            # 执行调度
            scheduled_tasks = schedulers[algorithm]([dict(task) for task in tasks])
            
            # 记录调度结果
            for task in scheduled_tasks:
                db.execute('''
                    INSERT INTO scheduler_results (
                        task_id, start_time, end_time, status, algorithm, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    task['task_id'],
                    task['start_time'],
                    task['end_time'],
                    task['status'],
                    algorithm,
                    now.isoformat()
                ))
            
            db.commit()
            return scheduled_tasks
        except Exception as e:
            print(f"调度任务失败: {str(e)}")
            return [] 