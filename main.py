from fastapi import FastAPI, Form, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()


# 获取数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 基础接口
@app.get("/")
def home():
    return {"message": "Hello FastAPI 全栈项目！"}


@app.get("/user")
def get_user():
    return {
        "username": "fastapi_user",
        "age": 20,
        "email": "user@example.com"
    }


@app.get("/greet")
def greet(name: str):
    return {"message": f"你好 {name}！欢迎使用 FastAPI"}


# 前端页面（带表单）
@app.get("/page", response_class=HTMLResponse)
def index_page():
    html_content = """
    <html>
        <head>
            <title>FastAPI 全栈页面</title>
            <style>
                body { font-family: 微软雅黑; margin: 40px; }
                .box { padding: 20px; background: #f5f5f5; border-radius: 8px; max-width: 400px; }
                input { padding: 8px; margin: 5px; width: 200px; }
                button { padding: 8px 16px; background: #4285f4; color: white; border: none; border-radius: 4px; }
            </style>
        </head>
        <body>
            <h1>✅ FastAPI 全栈项目</h1>
            <div class="box">
                <h3>用户信息表单</h3>
                <form action="/submit" method="post">
                    <input type="text" name="username" placeholder="输入姓名" required><br>
                    <input type="number" name="age" placeholder="输入年龄" required><br>
                    <button type="submit">提交并保存到数据库</button>
                </form>
            </div>
        </body>
    </html>
    """
    return html_content


# 【核心功能】接收表单，存入数据库
@app.post("/submit")
def submit_form(
        username: str = Form(...),
        age: int = Form(...),
        db: Session = Depends(get_db)
):
    # 1. 创建用户对象
    user = User(username=username, age=age)

    # 2. 加入数据库
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "msg": "用户已保存到数据库",
        "id": user.id,
        "username": user.username,
        "age": user.age
    }


# 新增：查看所有数据库里的用户
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

# 新增：页面版 —— 查看所有用户（从数据库读取）
@app.get("/users_page", response_class=HTMLResponse)
def show_users_page(db: Session = Depends(get_db)):
    users = db.query(User).all()

    # 拼接用户列表 HTML
    user_items = ""
    for user in users:
        user_items += f"<li>ID：{user.id} | 姓名：{user.username} | 年龄：{user.age}</li>"

    html = f"""
    <html>
        <head>
            <title>用户列表</title>
            <style>
                body {{ font-family: 微软雅黑; margin: 40px; }}
                .box {{ padding: 20px; background: #f5f5f5; border-radius: 8px; max-width: 500px; }}
                li {{ margin: 8px 0; font-size: 16px; }}
            </style>
        </head>
        <body>
            <h1>📋 数据库用户列表</h1>
            <div class="box">
                <ul>
                    {user_items}
                </ul>
                <br>
                <a href="/page">返回表单页面</a>
            </div>
        </body>
    </html>
    """
    return html