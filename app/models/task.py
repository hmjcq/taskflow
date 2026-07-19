# app/models/task.py
from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin

class Task(TimestampMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "status IN ('TODO', 'IN_PROGRESS', 'DONE')",
            name="chk_status"
        ),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment="任务标题")
    description = Column(Text, comment="详细描述")
    status = Column(
        String(20),
        nullable=False,
        default="TODO",
        index=True,   # 经常按状态筛选
        comment="任务状态：TODO / IN_PROGRESS / DONE"
    )
    priority = Column(Integer, nullable=False, default=0, comment="优先级，数值越大越紧急")
    due_date = Column(DateTime(timezone=True), comment="截止日期")
    category_id = Column(
        BigInteger,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="所属分类 ID，可为空"
    )
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属用户 ID"
    )

    # ========== 关系定义 ==========
    # 一个任务属于一个分类（可选）
    category = relationship("Category", back_populates="tasks")

    # 一个任务属于一个用户
    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"