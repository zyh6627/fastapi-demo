from pathlib import Path
from fastapi import FastAPI, Form, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from uuid import uuid4
from jinja2 import Environment, FileSystemLoader

from database import engine, SessionLocal
from models import Base, User
from utils import get_password_hash, verify_password

_tpl_env = Environment(loader=FileSystemLoader(str(Path(__file__).parent / "templates")))

def render(name: str, context: dict) -> HTMLResponse:
    template = _tpl_env.get_template(name)
    return HTMLResponse(template.render(**context))

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

@app.get("/page")
def page():
    return render("index.html", {})

@app.post("/register")
def register(username: str=Form(...), age:int=Form(...), password:str=Form(...), db:Session=Depends(get_db)):
    if db.query(User).filter(User.username==username).first():
        raise HTTPException(400, detail="用户名已存在")
    u = User(username=username, age=age, password=get_password_hash(password))
    db.add(u)
    db.commit()
    return {"msg":"注册成功"}

@app.post("/login")
def login(username:str=Form(...), password:str=Form(...), db:Session=Depends(get_db)):
    u = db.query(User).filter(User.username==username).first()
    if not u or not verify_password(password, u.password):
        return render("login_result.html", {"success": False, "message": "账号密码错误"})
    token = str(uuid4())
    login_users[token] = username
    res = render("login_result.html", {"success": True, "message": "登录成功"})
    res.set_cookie("token", token)
    return res

@app.get("/users_page")
def users_page(db:Session=Depends(get_db), name=Depends(require_login)):
    users = db.query(User).all()
    return render("users.html", {"username": name, "users": users})