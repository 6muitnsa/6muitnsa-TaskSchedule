from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ...schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from ...services.task_service import TaskService
from ...db.session import get_db
from ...models.task import TaskStatus, TimeStatus

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    return await task_service.create_task(task)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[TaskStatus] = None,
    time_status: Optional[TimeStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    tasks = await task_service.get_tasks(skip, limit, status, time_status)
    total = len(tasks)
    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    updated_task = await task_service.update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status: TaskStatus,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    updated_task = await task_service.update_task_status(task_id, status)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.patch("/{task_id}/priority", response_model=TaskResponse)
async def update_task_priority(
    task_id: int,
    priority: int,
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    updated_task = await task_service.update_task_priority(task_id, priority)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task 