from fastapi import FastAPI
from fastapi.responses import HTMLResponse  # 导入HTML支持

app = FastAPI()

# 1. 后端API接口：返回JSON
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

# 2. 前端页面：返回网页（这就是全栈！）
@app.get("/page", response_class=HTMLResponse)
def index_page():
    # 直接返回HTML代码
    html_content = """
    <html>
        <head>
            <title>FastAPI 全栈页面</title>
            <style>
                body { font-family: 微软雅黑; margin: 40px; }
                .box { padding: 20px; background: #f5f5f5; border-radius: 8px; }
            </style>
        </head>
        <body>
            <h1>✅ FastAPI 全栈项目运行成功</h1>
            <div class="box">
                <p>这是前端页面</p>
                <p>接口数据：<a href="/user">查看用户信息</a></p>
            </div>
        </body>
    </html>
    """
    return html_content