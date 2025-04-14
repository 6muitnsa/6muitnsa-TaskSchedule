from pydantic import BaseModel
from typing import List
from datetime import datetime

class ScheduleRequest(BaseModel):
    algorithm: str
    tasks: List[dict]

class ScheduledTask(BaseModel):
    id: str
    name: str
    start_time: datetime
    end_time: datetime
    estimated_time: int
    priority: int

class ScheduleEvaluation(BaseModel):
    total_time: float
    average_waiting_time: float
    average_turnaround_time: float
    efficiency: float

class ScheduleResult(BaseModel):
    scheduled_tasks: List[ScheduledTask]
    evaluation: ScheduleEvaluation 