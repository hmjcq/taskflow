from fastapi import FastAPI
from app.api.v1 import auth, users

app = FastAPI(title="TaskFlow", version="1.0.0")

# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
