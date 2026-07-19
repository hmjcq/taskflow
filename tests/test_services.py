import pytest
from fastapi import HTTPException
from app.services.auth_service import AuthService

def test_register_success(db):
    user = AuthService.register(db, "testuser", "test@t.com", "12345678")
    assert user.username == "testuser"

def test_register_duplicate_username(db):
    AuthService.register(db, "dup", "a@a.com", "12345678")
    with pytest.raises(HTTPException) as e:
        AuthService.register(db, "dup", "b@b.com", "12345678")
    assert e.value.status_code == 409

def test_register_duplicate_email(db):
    AuthService.register(db, "u1", "same@x.com", "12345678")
    with pytest.raises(HTTPException):
        AuthService.register(db, "u2", "same@x.com", "12345678")

def test_login_success(db):
    AuthService.register(db, "john", "john@x.com", "12345678")
    result = AuthService.login_by_username(db, "john", "12345678")
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert result["user"].username == "john"

def test_login_wrong_password(db):
    AuthService.register(db, "jane", "jane@x.com", "12345678")
    with pytest.raises(HTTPException) as e:
        AuthService.login_by_username(db, "jane", "wrong")
    assert e.value.status_code == 401