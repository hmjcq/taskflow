from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin

class Task(TimestampMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("status IN ('TODO', 'IN_PROGRESS', 'DONE')", name="chk_status"),
        Index("idx_user_status", "user_id", "status"),          # 按用户+状态过滤
        Index("idx_user_priority", "user_id", "priority"),      # 按用户+优先级排序/过滤
        Index("idx_user_duedate", "user_id", "due_date"),       # 按用户+截止时间排序
        Index("idx_user_category", "user_id", "category_id"),   # 按分类过滤
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)     # 搜索字段加索引
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="TODO")
    priority = Column(BigInteger, nullable=False, default=0)
    due_date = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(BigInteger, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")