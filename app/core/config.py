# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库连接字符串
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/taskflow"
    # JWT 密钥
    SECRET_KEY: str = "change-me-in-production"
    # JWT 过期时间（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

# ！！！这一行绝对不能少 ！！！
settings = Settings()