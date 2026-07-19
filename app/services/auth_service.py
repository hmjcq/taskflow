# app/services/auth_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import create_user, get_user_by_username, get_user_by_email
from app.utils.security import verify_password
from app.core.security import create_access_token
from app.models.user import User

class AuthService:
    """用户认证业务逻辑"""

    @staticmethod
    def register(db: Session, username: str, email: str, password: str) -> User:
        """
        注册新用户。
        1. 检查用户名是否已存在
        2. 检查邮箱是否已存在
        3. 创建用户（密码在 CRUD 层加密）
        4. 返回新用户实例
        """
        if get_user_by_username(db, username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="用户名已被注册"
            )
        if get_user_by_email(db, email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="邮箱已被注册"
            )
        user = create_user(db, username=username, email=email, password=password)
        return user

    @staticmethod
    def login_by_username(db: Session, username: str, password: str) -> dict:
        """
        使用用户名登录。
        1. 查询用户
        2. 检查存在性和激活状态
        3. 验证密码
        4. 生成 JWT
        5. 返回 token 和用户信息
        """
        user = get_user_by_username(db, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被禁用"
            )
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user,
        }

    @staticmethod
    def login(db: Session, login: str, password: str) -> dict:
        """
        用户登录（支持邮箱或用户名）。
        """
        if "@" in login:
            user = get_user_by_email(db, login)
        else:
            user = get_user_by_username(db, login)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被禁用"
            )
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user,
        }