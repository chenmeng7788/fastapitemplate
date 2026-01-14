from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class User(Base):
    """用户模型"""
    full_name: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))  # 存储哈希后的密码