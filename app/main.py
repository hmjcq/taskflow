from fastapi import FastAPI
from app.database.session import engine
from app.models.base import Base

# 必须导入所有模型，确保关系正确配置
from app.models.user import User
from app.models.category import Category
from app.models.task import Task

Base.metadata.create_all(bind=engine)

app = FastAPI()

from app.api.v1 import auth, users, tasks
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")