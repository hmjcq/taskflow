# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 根据数据库类型，添加必要的连接参数（以 MySQL 和 SQLite 为例）
connect_args = {}
if "mysql" in SQLALCHEMY_DATABASE_URL:
    # MySQL 需要设定时区为 UTC，并启用传统时区模式，让 DateTime(timezone=True) 正常工作
    connect_args = {
        "init_command": "SET time_zone='+00:00'",   # 所有连接会话统一使用 UTC
    }
elif "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}      # SQLite 跨线程限制

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,          # 保留你原来的连接池设置
    max_overflow=20,
    connect_args=connect_args,   # 关键：把时区等参数传入
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()