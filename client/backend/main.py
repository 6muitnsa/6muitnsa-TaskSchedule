from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.tasks import router as tasks_router
from routers.settings import router as settings_router

app = FastAPI(title="TaskSchedule API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(settings_router, prefix="/api/settings", tags=["settings"])

@app.get("/")
async def root():
    return {"message": "Welcome to TaskSchedule API"} 