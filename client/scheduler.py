from datetime import datetime, timedelta
from typing import List, Dict
import heapq

class Task:
    def __init__(self, id: int, title: str, priority: int, duration: int,
                 start_time: datetime = None, end_time: datetime = None):
        self.id = id
        self.title = title
        self.priority = priority
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time

def schedule_tasks(tasks: List[Task], start_date: datetime, end_date: datetime) -> List[Dict]:
    """
    使用优先级调度算法安排任务
    
    Args:
        tasks: 任务列表
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        安排好的任务列表，包含开始时间和结束时间
    """
    # 按优先级排序任务
    tasks.sort(key=lambda x: (-x.priority, x.duration))
    
    # 初始化时间槽
    current_time = start_date
    scheduled_tasks = []
    
    for task in tasks:
        # 如果任务有固定的开始时间，直接使用
        if task.start_time:
            if task.start_time < start_date or task.start_time > end_date:
                continue
            current_time = task.start_time
        
        # 计算任务结束时间
        end_time = current_time + timedelta(minutes=task.duration)
        
        # 如果任务有固定的结束时间，检查是否冲突
        if task.end_time:
            if end_time > task.end_time:
                continue
            end_time = task.end_time
        
        # 检查是否超出调度时间范围
        if end_time > end_date:
            continue
        
        # 添加任务到调度列表
        scheduled_tasks.append({
            'id': task.id,
            'title': task.title,
            'start_time': current_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': task.duration,
            'priority': task.priority
        })
        
        # 更新当前时间
        current_time = end_time
    
    return scheduled_tasks

def optimize_schedule(scheduled_tasks: List[Dict], work_hours: Dict[str, List[int]]) -> List[Dict]:
    """
    优化任务调度，考虑工作时间
    
    Args:
        scheduled_tasks: 已调度的任务列表
        work_hours: 工作时间配置，格式为 {'weekday': [start_hour, end_hour]}
    
    Returns:
        优化后的任务列表
    """
    optimized_tasks = []
    
    for task in scheduled_tasks:
        start_time = datetime.fromisoformat(task['start_time'])
        end_time = datetime.fromisoformat(task['end_time'])
        
        # 获取工作日的工作时间
        weekday = start_time.strftime('%A').lower()
        if weekday in work_hours:
            work_start = work_hours[weekday][0]
            work_end = work_hours[weekday][1]
            
            # 调整任务开始时间到工作时间
            if start_time.hour < work_start:
                start_time = start_time.replace(hour=work_start, minute=0)
            elif start_time.hour >= work_end:
                # 如果任务开始时间在工作时间之后，移到下一天
                start_time = (start_time + timedelta(days=1)).replace(hour=work_start, minute=0)
            
            # 调整任务结束时间
            end_time = start_time + timedelta(minutes=task['duration'])
            if end_time.hour > work_end:
                # 如果任务结束时间在工作时间之后，移到下一天
                end_time = (end_time + timedelta(days=1)).replace(hour=work_start, minute=0)
        
        optimized_tasks.append({
            'id': task['id'],
            'title': task['title'],
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': task['duration'],
            'priority': task['priority']
        })
    
    return optimized_tasks 