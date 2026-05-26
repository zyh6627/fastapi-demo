from fastapi import FastAPI, Form, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from uuid import uuid4

from database import engine, SessionLocal
from models import Base, User
from utils import get_password_hash, verify_password

Base.metadata.create_all(bind=engine)
app = FastAPI()
login_users = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 权限校验（从Cookie拿token）
def require_login(token: str = Cookie(None)):
    if not token or token not in login_users:
        raise HTTPException(status_code=403, detail="请先登录")
    return login_users[token]

@app.get("/page", response_class=HTMLResponse)
def page():
    return HTMLResponse("""
    <html>
        <body>
        <h2>注册</h2>
        <form action="/register" method="post">
            <input name="username" placeholder="用户名" required><br>
            <input name="age" type="number" placeholder="年龄" required><br>
            <input name="password" type="password" placeholder="密码" required><br>
            <button>注册</button>
        </form>
        <hr>
        <h2>登录</h2>
        <form action="/login" method="post">
            <input name="username" placeholder="用户名" required><br>
            <input name="password" type="password" placeholder="密码" required><br>
            <button>登录</button>
        </form>
        </body>
    </html>
    """)

@app.post("/register")
def register(username: str=Form(...), age:int=Form(...), password:str=Form(...), db:Session=Depends(get_db)):
    if db.query(User).filter(User.username==username).first():
        raise HTTPException(400, detail="用户名已存在")
    u = User(username=username, age=age, password=get_password_hash(password))
    db.add(u)
    db.commit()
    return {"msg":"注册成功"}

@app.post("/login", response_class=HTMLResponse)
def login(username:str=Form(...), password:str=Form(...), db:Session=Depends(get_db)):
    u = db.query(User).filter(User.username==username).first()
    if not u or not verify_password(password, u.password):
        return HTMLResponse("<h3>账号密码错误</h3><a href='/page'>返回</a>")
    token = str(uuid4())
    login_users[token] = username
    res = HTMLResponse("<h3>登录成功</h3><a href='/users_page'>查看用户列表</a>")
    res.set_cookie("token", token)
    return res

@app.get("/users_page", response_class=HTMLResponse)
def users_page(db:Session=Depends(get_db), name=Depends(require_login)):
    users = db.query(User).all()
    li = "".join([f"<li>{u.id} - {u.username} - {u.age}</li>" for u in users])
    return HTMLResponse(f"<h3>欢迎 {name}</h3><ul>{li}</ul>")