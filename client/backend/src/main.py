from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import task_api, scheduler_api
from utils.database import init_db
import uvicorn
import sys

try:
    # 初始化数据库
    init_db()
except Exception as e:
    print(f"数据库初始化失败: {str(e)}")
    sys.exit(1)

app = FastAPI(
    title="Task Management System",
    description="A task management system with scheduling algorithms",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(task_api.router, prefix="/api")
app.include_router(scheduler_api.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Task Management System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 