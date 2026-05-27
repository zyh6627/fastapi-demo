# fastapi-demo

FastAPI 全栈入门项目：用户注册 / 登录 / 权限校验 / 用户列表。

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: Jinja2 模板 + 原生 CSS（响应式）
- **认证**: Cookie + Token（passlib sha256_crypt）

## 项目结构

```
.
├── main.py          # 应用入口，路由定义
├── models.py        # SQLAlchemy 数据模型
├── database.py      # 数据库连接配置
├── utils.py         # 密码加密 / 验证工具
└── templates/
    ├── index.html           # 注册 & 登录页
    ├── login_result.html    # 登录结果页
    └── users.html           # 用户列表页
```

## 快速启动

```bash
# 1. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 2. 安装依赖
pip install fastapi uvicorn sqlalchemy passlib jinja2 python-multipart

# 3. 启动服务
uvicorn main:app --reload
```

浏览器打开 http://127.0.0.1:8000/page

## API 路由

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/page` | 注册 & 登录页面 |
| POST | `/register` | 注册（username, age, password） |
| POST | `/login` | 登录，成功跳转用户列表 |
| GET | `/users_page` | 用户列表（需登录） |

## 数据库

首次启动自动创建 `fastapi.db`（SQLite），无需手动建表。
