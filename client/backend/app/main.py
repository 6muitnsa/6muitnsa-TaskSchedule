from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import tasks
from .db.session import engine
from .models import task
import asyncio

app = FastAPI(
    title="TaskSchedule API",
    description="智能时间管理优化系统API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.on_event("startup")
async def startup():
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(task.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to TaskSchedule API"} 