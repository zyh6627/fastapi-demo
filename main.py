from fastapi import FastAPI

app = FastAPI()

# 首页接口
@app.get("/")
def home():
    return {"message": "Hello FastAPI 全栈项目！"}

# 用户接口
@app.get("/user")
def get_user():
    return {
        "username": "fastapi_user",
        "age": 20,
        "email": "user@example.com"
    }

# 带参数接口
@app.get("/greet")
def greet(name: str):
    return {"message": f"你好 {name}！欢迎使用 FastAPI"}