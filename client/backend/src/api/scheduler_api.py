from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from services import scheduler_service
from utils.database import get_db
from schemas.scheduler import ScheduleRequest, ScheduleResult, ScheduleEvaluation

router = APIRouter()

@router.post("/schedule", response_model=ScheduleResult)
def schedule_tasks(request: ScheduleRequest, db: Session = Depends(get_db)):
    try:
        result = scheduler_service.schedule_tasks(
            db=db,
            algorithm=request.algorithm,
            tasks=request.tasks
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schedule/algorithms", response_model=List[str])
def get_available_algorithms():
    return scheduler_service.get_available_algorithms()

@router.post("/schedule/evaluate", response_model=ScheduleEvaluation)
def evaluate_schedule(request: ScheduleRequest, db: Session = Depends(get_db)):
    try:
        evaluation = scheduler_service.evaluate_schedule(
            db=db,
            tasks=request.tasks
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 