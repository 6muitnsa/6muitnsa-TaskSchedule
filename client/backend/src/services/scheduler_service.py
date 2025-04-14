from typing import List
from models.task import Task as TaskModel
from schemas.scheduler import ScheduleRequest, ScheduleResult, ScheduleEvaluation
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class Scheduler:
    def __init__(self):
        pass

    def schedule(self, tasks: List[TaskModel]) -> List[ScheduleResult]:
        raise NotImplementedError
    
    def evaluate(self, tasks: List[TaskModel]) -> ScheduleEvaluation:
        raise NotImplementedError

class FCFSScheduler(Scheduler):
    def schedule(self, tasks: List[TaskModel]) -> List[ScheduleResult]:
        results = []
        current_time = 0
        for task in tasks:
            if task.status == 'PENDING':
                results.append(ScheduleResult(
                    task_id=task.id,
                    start_time=current_time,
                    end_time=current_time + (task.estimated_time or 60),
                    actual_duration=task.estimated_time or 60
                ))
                current_time += task.estimated_time or 60
        return results
    
    def evaluate(self, tasks: List[TaskModel]) -> ScheduleEvaluation:
        total_time = 0
        waiting_time = 0
        turnaround_time = 0
        current_time = 0
        
        for task in tasks:
            if task.estimated_time:
                waiting_time += current_time
                total_time += task.estimated_time
                turnaround_time += current_time + task.estimated_time
                current_time += task.estimated_time
                
        return ScheduleEvaluation(
            total_time=total_time,
            average_waiting_time=waiting_time / len(tasks) if tasks else 0,
            average_turnaround_time=turnaround_time / len(tasks) if tasks else 0,
            efficiency=total_time / (current_time if current_time > 0 else 1)
        )

class SJFScheduler(Scheduler):
    def schedule(self, tasks: List[TaskModel]) -> List[ScheduleResult]:
        results = []
        current_time = 0
        sorted_tasks = sorted([t for t in tasks if t.status == 'PENDING'], key=lambda x: x.estimated_time or float('inf'))
        for task in sorted_tasks:
            results.append(ScheduleResult(
                task_id=task.id,
                start_time=current_time,
                end_time=current_time + (task.estimated_time or 60),
                actual_duration=task.estimated_time or 60
            ))
            current_time += task.estimated_time or 60
        return results
    
    def evaluate(self, tasks: List[TaskModel]) -> ScheduleEvaluation:
        total_time = 0
        waiting_time = 0
        turnaround_time = 0
        current_time = 0
        
        sorted_tasks = sorted([t for t in tasks if t.estimated_time], key=lambda x: x.estimated_time)
        for task in sorted_tasks:
            waiting_time += current_time
            total_time += task.estimated_time
            turnaround_time += current_time + task.estimated_time
            current_time += task.estimated_time
                
        return ScheduleEvaluation(
            total_time=total_time,
            average_waiting_time=waiting_time / len(tasks) if tasks else 0,
            average_turnaround_time=turnaround_time / len(tasks) if tasks else 0,
            efficiency=total_time / (current_time if current_time > 0 else 1)
        )

class RRScheduler(Scheduler):
    def __init__(self, time_slice: int = 10):
        self.time_slice = time_slice

    def schedule(self, tasks: List[TaskModel]) -> List[ScheduleResult]:
        results = []
        current_time = 0
        remaining_tasks = [(task, task.estimated_time or 60) for task in tasks if task.status == 'PENDING']

        while remaining_tasks:
            for i, (task, remaining_time) in enumerate(remaining_tasks[:]):
                if remaining_time <= self.time_slice:
                    results.append(ScheduleResult(
                        task_id=task.id,
                        start_time=current_time,
                        end_time=current_time + remaining_time,
                        actual_duration=remaining_time
                    ))
                    current_time += remaining_time
                    remaining_tasks.pop(i)
                else:
                    results.append(ScheduleResult(
                        task_id=task.id,
                        start_time=current_time,
                        end_time=current_time + self.time_slice,
                        actual_duration=self.time_slice
                    ))
                    current_time += self.time_slice
                    remaining_tasks[i] = (task, remaining_time - self.time_slice)

        return results
    
    def evaluate(self, tasks: List[TaskModel]) -> ScheduleEvaluation:
        total_time = 0
        waiting_time = 0
        turnaround_time = 0
        current_time = 0
        
        remaining_tasks = [(task, task.estimated_time or 60) for task in tasks if task.estimated_time]
        while remaining_tasks:
            for i, (task, remaining_time) in enumerate(remaining_tasks[:]):
                if remaining_time <= self.time_slice:
                    waiting_time += current_time
                    total_time += remaining_time
                    turnaround_time += current_time + remaining_time
                    current_time += remaining_time
                    remaining_tasks.pop(i)
                else:
                    waiting_time += current_time
                    total_time += self.time_slice
                    turnaround_time += current_time + self.time_slice
                    current_time += self.time_slice
                    remaining_tasks[i] = (task, remaining_time - self.time_slice)
                
        return ScheduleEvaluation(
            total_time=total_time,
            average_waiting_time=waiting_time / len(tasks) if tasks else 0,
            average_turnaround_time=turnaround_time / len(tasks) if tasks else 0,
            efficiency=total_time / (current_time if current_time > 0 else 1)
        )

def create_scheduler(algorithm: str) -> Scheduler:
    if algorithm == 'first-come-first-serve':
        return FCFSScheduler()
    elif algorithm == 'shortest-job-first':
        return SJFScheduler()
    elif algorithm == 'round-robin':
        return RRScheduler()
    else:
        raise ValueError(f"不支持的调度算法: {algorithm}")

def get_available_algorithms() -> List[str]:
    return ['first-come-first-serve', 'shortest-job-first', 'round-robin']

def schedule_tasks(db: Session, algorithm: str, tasks: List[TaskModel]) -> ScheduleResult:
    scheduler = create_scheduler(algorithm)
    scheduled_tasks = scheduler.schedule(tasks)
    evaluation = scheduler.evaluate(tasks)
    return ScheduleResult(
        scheduled_tasks=scheduled_tasks,
        evaluation=evaluation
    )

def evaluate_schedule(db: Session, tasks: List[TaskModel]) -> ScheduleEvaluation:
    scheduler = FCFSScheduler()  # 使用FCFS作为默认评估算法
    return scheduler.evaluate(tasks) 