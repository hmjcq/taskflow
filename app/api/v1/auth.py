# app/api/v1/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    注册新用户。
    """
    user = AuthService.register(db, user_in.username, user_in.email, user_in.password)
    return user

@router.post("/login", response_model=TokenResponse)
def login(login_in: LoginRequest, db: Session = Depends(get_db)):
    """
    使用用户名和密码登录，返回 JWT token。
    """
    result = AuthService.login_by_username(db, login_in.username, login_in.password)
    # 只返回 token 部分，user 信息由 /users/me 提供
    return {"access_token": result["access_token"], "token_type": result["token_type"]}