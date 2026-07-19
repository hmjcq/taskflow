import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import get_db
from app.models.base import Base

from app.models.user import User
from app.models.category import Category
from app.models.task import Task

import os
from dotenv import load_dotenv

load_dotenv(".env.test")

# 连接你的 MySQL 测试库（请按实际修改用户名、密码、端口）
SQLALCHEMY_TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    pool_pre_ping=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
        db.rollback()
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c