import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models import LocalTask, LocalPomodoro, SyncQueue
from config import SERVER_URL, SYNC_INTERVAL

class SyncManager:
    def __init__(self):
        self.session = None
        self.sync_task = None

    async def start_sync(self):
        if self.sync_task:
            return {"status": "already_running"}
        
        self.session = aiohttp.ClientSession()
        self.sync_task = asyncio.create_task(self._sync_loop())
        return {"status": "started"}

    async def stop_sync(self):
        if self.sync_task:
            self.sync_task.cancel()
            self.sync_task = None
        if self.session:
            await self.session.close()
            self.session = None

    async def _sync_loop(self):
        while True:
            try:
                await self._process_sync_queue()
                await asyncio.sleep(SYNC_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Sync error: {e}")
                await asyncio.sleep(SYNC_INTERVAL)

    async def _process_sync_queue(self, db: Session):
        # 获取待同步的任务
        pending_tasks = db.query(LocalTask).filter(
            LocalTask.sync_status == "pending"
        ).all()
        
        for task in pending_tasks:
            try:
                # 上传任务到服务器
                async with self.session.post(f"{SERVER_URL}/tasks/", json=self._format_task(task)) as response:
                    if response.status == 200:
                        task.sync_status = "synced"
                        task.last_sync = datetime.now()
                    else:
                        task.sync_status = "failed"
                db.commit()
            except Exception as e:
                task.sync_status = "failed"
                db.commit()
                print(f"Task sync error: {e}")

        # 获取待同步的番茄钟
        pending_pomodoros = db.query(LocalPomodoro).filter(
            LocalPomodoro.sync_status == "pending"
        ).all()
        
        for pomodoro in pending_pomodoros:
            try:
                # 上传番茄钟到服务器
                async with self.session.post(f"{SERVER_URL}/pomodoros/", json=self._format_pomodoro(pomodoro)) as response:
                    if response.status == 200:
                        pomodoro.sync_status = "synced"
                        pomodoro.last_sync = datetime.now()
                    else:
                        pomodoro.sync_status = "failed"
                db.commit()
            except Exception as e:
                pomodoro.sync_status = "failed"
                db.commit()
                print(f"Pomodoro sync error: {e}")

    async def pull_changes(self, db: Session):
        try:
            # 从服务器拉取任务更新
            async with self.session.get(f"{SERVER_URL}/tasks/") as response:
                if response.status == 200:
                    tasks = await response.json()
                    for task_data in tasks:
                        await self._update_local_task(db, task_data)

            # 从服务器拉取番茄钟更新
            async with self.session.get(f"{SERVER_URL}/pomodoros/") as response:
                if response.status == 200:
                    pomodoros = await response.json()
                    for pomodoro_data in pomodoros:
                        await self._update_local_pomodoro(db, pomodoro_data)
        except Exception as e:
            print(f"Pull changes error: {e}")

    async def _update_local_task(self, db: Session, task_data: Dict):
        task = db.query(LocalTask).filter(LocalTask.task_id == task_data["task_id"]).first()
        if task:
            # 更新现有任务
            for key, value in task_data.items():
                if key != "tags":
                    setattr(task, key, value)
            task.sync_status = "synced"
            task.last_sync = datetime.now()
        else:
            # 创建新任务
            task = LocalTask(
                task_id=task_data["task_id"],
                title=task_data["title"],
                description=task_data.get("description"),
                priority=task_data.get("priority", 0),
                status=task_data.get("status", "pending"),
                due_date=task_data.get("due_date"),
                sync_status="synced",
                last_sync=datetime.now()
            )
            db.add(task)
        db.commit()

    async def _update_local_pomodoro(self, db: Session, pomodoro_data: Dict):
        pomodoro = db.query(LocalPomodoro).filter(
            LocalPomodoro.pomodoro_id == pomodoro_data["pomodoro_id"]
        ).first()
        if pomodoro:
            # 更新现有番茄钟
            for key, value in pomodoro_data.items():
                setattr(pomodoro, key, value)
            pomodoro.sync_status = "synced"
            pomodoro.last_sync = datetime.now()
        else:
            # 创建新番茄钟
            pomodoro = LocalPomodoro(
                pomodoro_id=pomodoro_data["pomodoro_id"],
                task_id=pomodoro_data["task_id"],
                start_time=pomodoro_data["start_time"],
                end_time=pomodoro_data.get("end_time"),
                duration=pomodoro_data["duration"],
                type=pomodoro_data["type"],
                completed=pomodoro_data.get("completed", False),
                sync_status="synced",
                last_sync=datetime.now()
            )
            db.add(pomodoro)
        db.commit()

    def _format_task(self, task: LocalTask) -> Dict:
        tags = [tag.tag for tag in task.tags]
        return {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date,
            "tags": tags
        }

    def _format_pomodoro(self, pomodoro: LocalPomodoro) -> Dict:
        return {
            "pomodoro_id": pomodoro.pomodoro_id,
            "task_id": pomodoro.task_id,
            "start_time": pomodoro.start_time,
            "end_time": pomodoro.end_time,
            "duration": pomodoro.duration,
            "type": pomodoro.type,
            "completed": pomodoro.completed
        } 