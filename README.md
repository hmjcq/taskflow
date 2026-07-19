# TaskFlow

> A modern enterprise-grade task management backend built with **FastAPI**, **SQLAlchemy**, **MySQL**, and **JWT Authentication**.

TaskFlow 是一个基于 FastAPI 开发的企业级任务管理系统，采用经典分层架构设计，实现了完整的用户认证、任务管理、权限控制及 RESTful API，为 Python 后端开发实践提供了完整示例。

---

## Features

-  JWT 用户认证与权限控制
-  用户注册、登录、身份验证
-  Task 任务 CRUD
-  任务搜索、过滤、分页、排序
-  SQLAlchemy ORM 数据持久化
-  Alembic 数据库迁移
-  Pytest 自动化测试
-  Swagger(OpenAPI) 在线接口文档
-  分层架构，便于维护与扩展


## Tech Stack

| Category | Technology |
|------------|------------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | MySQL 8 |
| Authentication | JWT (python-jose) |
| Password Encryption | bcrypt |
| Migration | Alembic |
| Validation | Pydantic |
| Testing | Pytest |
| Documentation | Swagger / OpenAPI |

---

## Project Structure

```text
TaskFlow
│
├── app
│   ├── api              # RESTful API
│   ├── core             # Config / JWT / Settings
│   ├── crud             # Database Operations
│   ├── database         # Database Session
│   ├── models           # SQLAlchemy Models
│   ├── schemas          # Pydantic Schemas
│   ├── services         # Business Logic
│   ├── utils            # Utility Functions
│   └── main.py
│
├── alembic              # Database Migration
├── tests                # Unit Tests
├── docs                 # Project Images
├── requirements.txt
└── README.md
```

---

## Database Design

Current Version：

- User
- Task
- Category

Relationship：

```text
User
 └──────< Task >────── Category
```

---

## REST API

启动后访问：

```
http://127.0.0.1:8000/docs
```

即可查看完整 Swagger 文档。

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/auth/register | Register |
| POST | /api/v1/auth/login | Login |
| GET | /api/v1/users/me | Current User |

### Task

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/tasks | Get Tasks |
| POST | /api/v1/tasks | Create Task |
| GET | /api/v1/tasks/{id} | Get Task |
| PUT | /api/v1/tasks/{id} | Update Task |
| DELETE | /api/v1/tasks/{id} | Delete Task |

Supports：

- Pagination
- Search
- Filter
- Sorting

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/hmjcq/taskflow.git
cd taskflow
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
```

Linux / macOS：

```bash
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file.

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/taskflow

SECRET_KEY=your-secret-key
```

---

### 5. Create Database

```sql
CREATE DATABASE taskflow
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

### 6. Run Server

```bash
uvicorn app.main:app --reload
```

Open：

```
http://127.0.0.1:8000/docs
```

---

## Testing

Run：

```bash
pytest
```

Example：

```text
=============================
17 passed
=============================
```

---

## Roadmap

- [ ] Docker Deployment
- [ ] Redis Cache
- [ ] GitHub Actions CI
- [ ] Email Notification
- [ ] File Upload
- [ ] Team Collaboration
- [ ] Vue / React Frontend

---

## Project Highlights

- Enterprise layered architecture
- RESTful API design
- JWT authentication
- Password hashing with bcrypt
- SQLAlchemy ORM
- Alembic migration
- Automated testing
- OpenAPI documentation

---

## License

This project is licensed under the MIT License.

---

## Author

**清夕雨**

- GitHub：https://github.com/hmjcq