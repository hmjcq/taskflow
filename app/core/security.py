# app/core/security.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    生成 JWT access token
    :param data: 要编码进 token 的数据（如 {"sub": user.id}）
    :param expires_delta: 过期时间增量，默认使用配置中的 ACCESS_TOKEN_EXPIRE_MINUTES
    :return: JWT 字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    解码并验证 JWT token，成功返回 payload 字典，失败返回 None
    :param token: JWT 字符串
    :return: 解码后的 payload 或 None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None