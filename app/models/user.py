# app/models/user.py (最终完整版)
from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # 关系
    categories = relationship("Category", back_populates="user", lazy="dynamic")
    tasks = relationship("Task", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"