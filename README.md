# 数据库迁移
## 核心依赖
pip install fastapi sqlalchemy alembic

## 数据库驱动（根据需要选择）
pip install aiomysql PyMySQL          # MySQL
pip install asyncpg psycopg2-binary   # PostgreSQL  
pip install aiosqlite                 # SQLite

## Alembic配置
### 1. 初始化Alembic
### 在项目根目录执行
``alembic init migrations``

### 2. 配置数据库连接
修改   alembic/env.py

# 生成与执行迁移脚本
### 1. 首次生成迁移脚本（创建表）
``alembic revision --autogenerate -m "初始化数据库，创建用户表" ``

#### 执行后，alembic/versions/ 目录会生成一个带时间戳的脚本（如 20241029_123456_初始化数据库，创建用户表.py）。
#### 检查脚本内容是否正确（尤其 upgrade() 方法是否包含创建 user 表的逻辑）。

### 2. 执行迁移（应用到数据库）
``alembic upgrade head``

### 3. 后续修改模型（如新增字段）
#### 例如，在 User 模型中新增 is_active 字段：
```bash
class User(Base):
    # ... 原有字段
    is_active: Mapped[bool] = mapped_column(default=True)  # 新增字段
```
#### 生成新的迁移脚本：
``alembic revision --autogenerate -m "用户表新增 is_active 字段"``
#### 执行迁移
``alembic upgrade head``
### 4 回滚操作（如需撤销）
```bash
alembic downgrade -1  # 回滚到上一个版本
alembic downgrade base  # 回滚到初始状态（删除所有表）
```

# 迁移命令
```bash
# 升级到最新版本
alembic upgrade head

# 升级到特定版本
alembic upgrade <revision_id>

# 降级到前一个版本
alembic downgrade -1

# 降级到特定版本
alembic downgrade <revision_id>

# 查看当前版本
alembic current

# 查看迁移历史
alembic history

# 查看详细历史
alembic history --verbose
```


# fastapi 启动
### 使用 uvicorn 启动时，通过 --env-file 加载对应环境的配置文件：
```bash
# 开发环境（加载 .env.dev）
uvicorn app.main:app --reload --env-file .env.dev

# 生产环境（加载 .env.prod）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file .env
```

### 在服务器的启动脚本中设置环境变量（无需 .env 文件）：
```bash
# 生产环境启动脚本（示例）
export ENVIRONMENT=prod
export DATABASE_URL=postgresql://prod_user:xxx@prod-db:5432/prod_db
export SECRET_KEY=xxx...
uvicorn app.main:app --host 0.0.0.0 --port 8000
```