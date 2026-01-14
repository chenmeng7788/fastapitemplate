from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# 创建 MySQL 引擎（SQLAlchemy 连接池配置）
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 连接前检查可用性
    pool_recycle=3600,   # 1小时后回收连接（避免 MySQL 8小时超时）
)

# 会话工厂（每次请求创建一个会话）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)