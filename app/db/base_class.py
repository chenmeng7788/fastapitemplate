from sqlalchemy import MetaData, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

# 数据库对象命名约定（索引、外键等）
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    """所有模型的基类，包含通用字段"""
    metadata = metadata

    # 自动生成表名（类名小写）
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # 通用字段：主键、创建时间、更新时间
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )