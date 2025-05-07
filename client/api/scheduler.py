from datetime import datetime, timedelta
import json

class Scheduler:
    def __init__(self, algorithm='FCFS', time_slice=25):
        self.algorithm = algorithm
        self.time_slice = time_slice  # 时间片大小（分钟）
    
    def schedule(self, tasks):
        if not tasks:
            return []
        
        # 转换任务格式
        tasks = [self._convert_task(task) for task in tasks]
        
        # 根据算法选择调度方法
        if self.algorithm == 'FCFS':
            return self._fcfs(tasks)
        elif self.algorithm == 'SJF':
            return self._sjf(tasks)
        elif self.algorithm == 'Priority':
            return self._priority(tasks)
        elif self.algorithm == 'RR':
            return self._rr(tasks)
        else:
            return self._fcfs(tasks)  # 默认使用FCFS
    
    def _convert_task(self, task):
        """转换任务格式"""
        return {
            'id': task['id'],
            'name': task['name'],
            'start_time': datetime.fromisoformat(task['start_time']),
            'estimated_duration': task.get('estimated_duration', 0),
            'priority': self._get_priority_value(task.get('priority', '中')),
            'status': task['status']
        }
    
    def _get_priority_value(self, priority):
        """获取优先级数值"""
        priority_map = {
            '高': 3,
            '中': 2,
            '低': 1
        }
        return priority_map.get(priority, 2)
    
    def _fcfs(self, tasks):
        """先来先服务算法"""
        return sorted(tasks, key=lambda x: x['start_time'])
    
    def _sjf(self, tasks):
        """最短作业优先算法"""
        return sorted(tasks, key=lambda x: (x['start_time'], x['estimated_duration']))
    
    def _priority(self, tasks):
        """优先级调度算法"""
        return sorted(tasks, key=lambda x: (x['start_time'], -x['priority']))
    
    def _rr(self, tasks):
        """时间片轮转算法"""
        if not tasks:
            return []
        
        # 按到达时间排序
        tasks = sorted(tasks, key=lambda x: x['start_time'])
        result = []
        current_time = tasks[0]['start_time']
        
        while tasks:
            task = tasks.pop(0)
            if task['estimated_duration'] <= self.time_slice:
                # 任务可以在一个时间片内完成
                result.append(task)
                current_time += timedelta(minutes=task['estimated_duration'])
            else:
                # 任务需要多个时间片
                task['estimated_duration'] -= self.time_slice
                current_time += timedelta(minutes=self.time_slice)
                tasks.append(task)
        
        return result 