def test_register_api(client, db):
    resp = client.post("/api/v1/auth/register", json={
        "username": "api_user",
        "email": "api@t.com",
        "password": "12345678",
        "password_confirm": "12345678"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "api_user"
    assert "id" in data
    assert "password_hash" not in data

def test_login_api(client, db):
    # 先注册
    client.post("/api/v1/auth/register", json={
        "username": "login_user",
        "email": "login@t.com",
        "password": "12345678",
        "password_confirm": "12345678"
    })
    # 登录
    resp = client.post("/api/v1/auth/login", json={
        "username": "login_user",
        "password": "12345678"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_users_me(client, db):
    # 注册并登录获取 token
    client.post("/api/v1/auth/register", json={
        "username": "me_user",
        "email": "me@t.com",
        "password": "12345678",
        "password_confirm": "12345678"
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "me_user",
        "password": "12345678"
    })
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/v1/users/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "me_user"

def test_users_me_unauthenticated(client):
    resp = client.get("/api/v1/users/me")
    assert resp.status_code == 401