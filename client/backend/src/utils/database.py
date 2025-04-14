from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from models.task import Base, Task
from models.schedule import Schedule
from models.user_preference import UserPreference

# 获取数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'task_manager.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite特定参数
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        # 确保数据库目录存在
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"创建数据库目录: {db_dir}")
        
        # 创建表（如果不存在会自动创建）
        Base.metadata.create_all(bind=engine)
        print(f"数据库初始化完成: {DB_PATH}")
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        raise

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 