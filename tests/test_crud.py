import pytest
from app.crud.user import create_user, get_user_by_username, get_user_by_email

def test_create_user(db):
    user = create_user(db, "test", "test@example.com", "pass12345678")
    assert user.id is not None
    assert user.username == "test"

def test_get_user_by_username(db):
    create_user(db, "alice", "alice@x.com", "pass12345678")
    u = get_user_by_username(db, "alice")
    assert u is not None
    assert u.email == "alice@x.com"
    assert get_user_by_username(db, "nobody") is None

def test_get_user_by_email(db):
    create_user(db, "bob", "bob@x.com", "pass12345678")
    u = get_user_by_email(db, "bob@x.com")
    assert u is not None
    assert u.username == "bob"
    assert get_user_by_email(db, "no@no.com") is None