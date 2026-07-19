# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password

def create_user(db: Session, username: str, email: str, password: str) -> User:
    """
    创建新用户并保存到数据库。
    密码通过 hash_password 加密，存储的是 bcrypt 哈希。
    返回已创建的 User 实例（已包含自增 ID 等）。
    """
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)   # 密码绝不存明文
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str) -> User | None:
    """根据用户名精确查询用户，未找到返回 None"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    """根据邮箱精确查询用户，未找到返回 None"""
    return db.query(User).filter(User.email == email).first()