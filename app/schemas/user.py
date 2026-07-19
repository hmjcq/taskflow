# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

# ---------- 用户注册 ----------
class UserCreate(BaseModel):
    """用于 POST /register 的请求体"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=8, max_length=128, description="明文密码（后端会加密）")
    # 可选：确认密码
    password_confirm: str = Field(..., min_length=8, max_length=128, description="再次输入密码")

    @validator("password_confirm")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("两次输入的密码不一致")
        return v

    # 注册完成后，后端只返回 UserResponse，因此这个 Schema 仅用于输入


# ---------- 用户登录 ----------
class UserLogin(BaseModel):
    """用于 POST /login 的请求体，支持用 用户名 或 邮箱 登录"""
    login: str = Field(..., description="用户名或邮箱地址")
    password: str = Field(..., min_length=8, max_length=128, description="明文密码")


# ---------- 用户响应（公共） ----------
class UserResponse(BaseModel):
    """返回给前端的用户公开信息，绝不包含密码哈希"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        # 允许从 ORM 对象自动转换
        from_attributes = True   # Pydantic v2 写法，v1 是 orm_mode = True

# ---------- 登录请求（严格版：只用 username）----------
class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="明文密码")

# ---------- JWT 令牌响应 ----------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"