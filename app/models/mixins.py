# app/models/mixins.py
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class TimestampMixin:
    """所有需要自动记录创建/更新时间的模型都继承这个 Mixin"""
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),    # 由数据库服务器端生成时间
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),          # 更新行时由数据库自动更新时间
        nullable=False,
    )