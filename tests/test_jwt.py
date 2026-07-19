from app.core.security import create_access_token, decode_access_token
from datetime import timedelta

def test_create_and_decode_token():
    data = {"sub": "1"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "1"

def test_decode_expired_token():
    from datetime import datetime, timezone
    data = {"sub": "1"}
    # 马上过期
    token = create_access_token(data, expires_delta=timedelta(seconds=-1))
    payload = decode_access_token(token)
    assert payload is None

def test_decode_invalid_token():
    assert decode_access_token("garbage") is None