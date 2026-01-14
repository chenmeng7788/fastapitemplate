"""Alembic 环境配置"""

import os
import sys
from logging.config import fileConfig
from pathlib import Path
from sqlalchemy import pool, create_engine
from alembic import context
from dotenv import load_dotenv
# 在导入模型的位置添加自动导入逻辑
import pkgutil


# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量（可选，若已在 alembic.ini 中配置则可跳过）
load_dotenv(project_root / ".env")

from app.db.base_class import Base

# 自动导入 app/db/models 目录下的所有模型模块
models_dir = project_root / "app" / "models"
for module_info in pkgutil.iter_modules([str(models_dir)]):
    if not module_info.ispkg:
        # 导入模块（如 app.models.user）
        __import__(f"app.models.{module_info.name}", globals(), locals(), [], 0)

# 目标元数据（Base 的元数据，包含所有模型信息）
target_metadata = Base.metadata

# ... 保留其他默认配置（如下）



def run_migrations_online():
    # 从环境变量获取数据库连接 URL（替代 alembic.ini 中的配置）
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL 环境变量未设置，请检查 .env 文件")

    # 使用环境变量的 URL 创建连接引擎
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
        pool_pre_ping=True,  # 增加连接可用性检查
    )


    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # 启用命名约定（与 Base 中的 convention 对应）
            version_table_schema=target_metadata.schema,
            render_as_batch=True,  # 支持 MySQL 等不支持 ALTER TABLE 的数据库批量修改
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()