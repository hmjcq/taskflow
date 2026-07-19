import pytest
from app.utils.security import hash_password, verify_password

def test_hash_and_verify():
    plain = "mysecret"
    hashed = hash_password(plain)
    assert isinstance(hashed, str)
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_hash_is_different_each_time():
    plain = "mysecret"
    h1 = hash_password(plain)
    h2 = hash_password(plain)
    # bcrypt 每次加盐不同，哈希值不同
    assert h1 != h2
    assert verify_password(plain, h1)
    assert verify_password(plain, h2)