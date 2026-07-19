# app/utils/security.py
import bcrypt

def hash_password(password: str) -> str:
    """
    对明文密码进行 bcrypt 哈希，返回哈希字符串。
    整个项目中，任何需要存储密码的地方都必须调用此函数。
    """
    # bcrypt.hashpw 要求输入 bytes，输出 bytes
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码是否与数据库中存储的 bcrypt 哈希匹配。
    用于登录验证，绝不进行明文比对。
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )