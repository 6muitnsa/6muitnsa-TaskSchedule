from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import task_api
from src.models.task import Base
from src.utils.database import engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="智能时间管理优化系统",
    description="基于调度算法的时间管理工具",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允许的前端域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# 注册路由
app.include_router(task_api.router, prefix="/api", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "欢迎使用智能时间管理优化系统"} 