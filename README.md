# TaskFlow

> 个人任务管理 API，基于 FastAPI + MySQL，支持 JWT 认证、任务增删改查、搜索、分页与排序。

![TaskFlow Banner](docs/banner.png)

## 功能演示

| 用户注册与登录 | 任务 CRUD | 搜索与过滤 |
|:---:|:---:|:---:|
| ![注册](docs/screenshots/register.png) | ![任务列表](docs/screenshots/tasks.png) | ![搜索](docs/screenshots/search.png) |

## 技术栈

- **后端框架**: FastAPI (Python 3.11+)
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (python-jose) + bcrypt
- **文档**: 自动生成 Swagger UI (OpenAPI)
- **代码质量**: Black, isort

## 项目架构
TaskFlow/
├── app/
│ ├── api/ # 路由层 (v1)
│ ├── core/ # 配置、JWT
│ ├── crud/ # 数据库操作
│ ├── models/ # SQLAlchemy 模型
│ ├── schemas/ # Pydantic 校验
│ ├── services/ # 业务逻辑
│ ├── database/ # 数据库连接
│ └── utils/ # 工具 (密码哈希)
├── tests/ # 单元测试 & 集成测试
├── .env.example # 环境变量模板
├── requirements.txt
└── README.md


## 接口文档

启动项目后访问 `http://127.0.0.1:8000/docs` 查看完整的 Swagger API 文档。

主要端点：
- `POST /api/v1/auth/register`  注册
- `POST /api/v1/auth/login`     登录
- `GET /api/v1/users/me`        当前用户信息
- `GET /api/v1/tasks`           任务列表（分页、搜索、排序、过滤）
- `POST /api/v1/tasks`          创建任务
- `GET /api/v1/tasks/{id}`      获取任务详情
- `PUT /api/v1/tasks/{id}`      更新任务
- `DELETE /api/v1/tasks/{id}`   删除任务

## 快速启动

### 1. 克隆仓库
```bash
git clone https://github.com/hmjcq/taskflow.git
cd taskflow

2. 安装依赖
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

3. 配置环境变量
复制 .env.example 为 .env，修改数据库连接和 JWT 密钥：
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/taskflow
SECRET_KEY=your-secret-key-here

4. 创建数据库
在 MySQL 中执行：
CREATE DATABASE taskflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

5. 启动服务
uvicorn app.main:app --reload
打开浏览器访问 http://127.0.0.1:8000/docs 即可测试 API。

运行测试
# 确保测试数据库已创建（taskflow_test）
pytest

未来规划
标签、附件、评论功能

前端界面 (Vue/React)

团队协作与任务分配

定时提醒与通知

Docker 部署支持

License
本项目采用 MIT License

---