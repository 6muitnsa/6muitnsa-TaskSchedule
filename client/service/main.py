from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uvicorn

from models import LocalTask, LocalPomodoro, init_db
from task_manager import TaskManager
from pomodoro_manager import PomodoroManager
from sync_manager import SyncManager

app = FastAPI(title="TaskSchedule Client API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化管理器
task_manager = TaskManager()
pomodoro_manager = PomodoroManager()
sync_manager = SyncManager()

# 任务管理API
@app.post("/tasks/")
async def create_task(task: dict, db: Session = Depends(get_db)):
    return await task_manager.create_task(db, task)

@app.get("/tasks/")
async def get_tasks(db: Session = Depends(get_db)):
    return await task_manager.get_tasks(db)

@app.get("/tasks/{task_id}")
async def get_task(task_id: str, db: Session = Depends(get_db)):
    return await task_manager.get_task(db, task_id)

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: dict, db: Session = Depends(get_db)):
    return await task_manager.update_task(db, task_id, task)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    return await task_manager.delete_task(db, task_id)

# 番茄钟API
@app.post("/pomodoros/start/{task_id}")
async def start_pomodoro(task_id: str, db: Session = Depends(get_db)):
    return await pomodoro_manager.start_focus(db, task_id)

@app.post("/pomodoros/rest/")
async def start_rest(db: Session = Depends(get_db)):
    return await pomodoro_manager.start_rest(db)

@app.post("/pomodoros/extend/")
async def extend_pomodoro(minutes: int, db: Session = Depends(get_db)):
    return await pomodoro_manager.extend_time(db, minutes)

@app.post("/pomodoros/end/")
async def end_pomodoro(db: Session = Depends(get_db)):
    return await pomodoro_manager.end_current(db)

@app.get("/pomodoros/history/")
async def get_pomodoro_history(task_id: Optional[str] = None, db: Session = Depends(get_db)):
    return await pomodoro_manager.get_history(db, task_id)

# 同步API
@app.post("/sync/start/")
async def start_sync():
    return await sync_manager.start_sync()

@app.post("/sync/stop/")
async def stop_sync():
    return await sync_manager.stop_sync()

@app.post("/sync/pull/")
async def pull_changes(db: Session = Depends(get_db)):
    return await sync_manager.pull_changes(db)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 