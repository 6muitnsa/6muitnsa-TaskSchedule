from typing import List, Dict
from datetime import datetime, timedelta
from models import Task, Location, CommuteTime
from sqlalchemy.orm import Session

class Scheduler:
    def __init__(self, time_granularity: int = 30):
        self.time_granularity = time_granularity

    def calculate_commute_time(self, db: Session, from_location_id: int, to_location_id: int) -> int:
        """计算通勤时间"""
        commute = db.query(CommuteTime).filter(
            CommuteTime.from_location_id == from_location_id,
            CommuteTime.to_location_id == to_location_id
        ).first()
        return commute.default_minutes if commute else 30

    def schedule(self, tasks: List[Task], db: Session, start_time: datetime = None) -> List[Task]:
        """
        调度任务
        :param tasks: 待调度的任务列表
        :param db: 数据库会话
        :param start_time: 开始时间，默认为当前时间
        :return: 调度后的任务列表
        """
        if not tasks:
            return []
        
        if start_time is None:
            start_time = datetime.now()
        
        # 按优先级排序
        sorted_tasks = sorted(tasks, key=lambda x: x.priority, reverse=True)
        
        current_time = start_time
        last_location_id = None
        
        for task in sorted_tasks:
            if task.time_type == "fixed":
                continue  # 跳过固定时间的任务
            
            # 计算通勤时间
            if last_location_id and task.location_id:
                commute_time = self.calculate_commute_time(db, last_location_id, task.location_id)
                current_time += timedelta(minutes=commute_time)
            
            task.start_time = current_time
            task.end_time = current_time + timedelta(minutes=task.estimated_time)
            current_time = task.end_time
            last_location_id = task.location_id
        
        return sorted_tasks

class FCFSScheduler(Scheduler):
    """先来先服务调度算法"""
    def schedule(self, tasks: List[Task], db: Session, start_time: datetime = None) -> List[Task]:
        if not tasks:
            return []
        
        if start_time is None:
            start_time = datetime.now()
        
        # 按创建时间排序
        sorted_tasks = sorted(tasks, key=lambda x: x.created_at)
        
        current_time = start_time
        last_location_id = None
        
        for task in sorted_tasks:
            if task.time_type == "fixed":
                continue
            
            if last_location_id and task.location_id:
                commute_time = self.calculate_commute_time(db, last_location_id, task.location_id)
                current_time += timedelta(minutes=commute_time)
            
            task.start_time = current_time
            task.end_time = current_time + timedelta(minutes=task.estimated_time)
            current_time = task.end_time
            last_location_id = task.location_id
        
        return sorted_tasks

class SJFScheduler(Scheduler):
    """短作业优先调度算法"""
    def schedule(self, tasks: List[Task], db: Session, start_time: datetime = None) -> List[Task]:
        if not tasks:
            return []
        
        if start_time is None:
            start_time = datetime.now()
        
        # 按预计时间排序
        sorted_tasks = sorted(tasks, key=lambda x: x.estimated_time)
        
        current_time = start_time
        last_location_id = None
        
        for task in sorted_tasks:
            if task.time_type == "fixed":
                continue
            
            if last_location_id and task.location_id:
                commute_time = self.calculate_commute_time(db, last_location_id, task.location_id)
                current_time += timedelta(minutes=commute_time)
            
            task.start_time = current_time
            task.end_time = current_time + timedelta(minutes=task.estimated_time)
            current_time = task.end_time
            last_location_id = task.location_id
        
        return sorted_tasks

class RRScheduler(Scheduler):
    """轮转调度算法"""
    def __init__(self, time_granularity: int = 30, time_slice: int = 60):
        super().__init__(time_granularity)
        self.time_slice = time_slice

    def schedule(self, tasks: List[Task], db: Session, start_time: datetime = None) -> List[Task]:
        if not tasks:
            return []
        
        if start_time is None:
            start_time = datetime.now()
        
        # 按优先级分组
        priority_groups: Dict[int, List[Task]] = {}
        for task in tasks:
            if task.time_type == "fixed":
                continue
            if task.priority not in priority_groups:
                priority_groups[task.priority] = []
            priority_groups[task.priority].append(task)
        
        # 按优先级从高到低排序
        sorted_priorities = sorted(priority_groups.keys(), reverse=True)
        
        current_time = start_time
        last_location_id = None
        
        while any(len(group) > 0 for group in priority_groups.values()):
            for priority in sorted_priorities:
                group = priority_groups[priority]
                if not group:
                    continue
                
                task = group.pop(0)
                
                if last_location_id and task.location_id:
                    commute_time = self.calculate_commute_time(db, last_location_id, task.location_id)
                    current_time += timedelta(minutes=commute_time)
                
                task.start_time = current_time
                task.end_time = current_time + timedelta(minutes=min(task.estimated_time, self.time_slice))
                current_time = task.end_time
                last_location_id = task.location_id
                
                if task.estimated_time > self.time_slice:
                    task.estimated_time -= self.time_slice
                    group.append(task)
        
        return tasks

def get_scheduler(scheduler_type: str, time_granularity: int = 30) -> Scheduler:
    """获取指定类型的调度器"""
    schedulers = {
        "fcfs": FCFSScheduler,
        "sjf": SJFScheduler,
        "rr": RRScheduler,
        "default": Scheduler
    }
    scheduler_class = schedulers.get(scheduler_type, Scheduler)
    return scheduler_class(time_granularity=time_granularity) 