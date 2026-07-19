# app/models/category.py
from sqlalchemy import Column, BigInteger, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin

class Category(TimestampMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (
        # 同一用户下的分类名必须唯一
        UniqueConstraint("user_id", "name", name="uq_user_category"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True, comment="分类名称")
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属用户 ID"
    )

    # ========== 关系定义 ==========
    # 一个分类属于一个用户
    user = relationship("User", back_populates="categories")

    # 一个分类可以有多个任务
    tasks = relationship("Task", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"