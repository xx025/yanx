import os
import signal
import sys

import uvicorn
import webview
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from global_vals import global_vals
from global_vals import port
from yweb import yanx_app

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加 session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.include_router(yanx_app, prefix='/api')

# Mounting default static files
app.mount(path="/static", app=StaticFiles(directory=os.path.join('static')), name="static")

templates = Jinja2Templates(directory="template")
# 设置新的模板渲染标记
templates.env.block_start_string = "[%"
templates.env.block_end_string = "%]"
templates.env.variable_start_string = "[["
templates.env.variable_end_string = "]]"
templates.env.comment_start_string = "[#"
templates.env.comment_end_string = "#]"


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, 'title': 'YanX-研招网硕士专业目录下载'})


@app.get("/dl", response_class=HTMLResponse,
         description="会接收一些下载用的参数，这些参数将会存到 request.session 里面")
async def root2(request: Request,
                mllb: str,
                xklb: str,
                zymc: str = '',
                xxfs: str = '',
                yxjh: str = '',
                yxdq: str = ''):
    # 清空之前的 Session 中的 dlparams 数据
    global_vals['dlparams'] = []
    # 存储参数到 dlparams 字典
    dlparams = {
        "mllb": mllb,
        "xklb": xklb,
        "zymc": zymc,
        "xxfs": xxfs,
        "yxjh": yxjh,
        "yxdq": yxdq
    }
    global_vals["dlparams"] = dlparams  # 存储 dlparams 字典到 Session
    return templates.TemplateResponse("download.html",
                                      {"request": request,
                                       'title': 'YanX-研招网硕士专业目录下载'}
                                      )


@app.get('/open_link')
async def open_link(url: str):
    """
    不再程序内进行跳转链接，通过外部浏览器打开链接
    """
    import webbrowser
    webbrowser.open_new_tab(url)
    return {"message": f"已打开链接{url}"}


def start_server():
    # 创建文件夹，用于存放下载的文件
    os.makedirs('dldocs', exist_ok=True)
    # 启动 FastAPI
    uvicorn.run(app, host="localhost", port=port)


def on_closed():
    os.kill(os.getpid(), signal.SIGTERM)
    print("窗口关闭，退出程序")


if __name__ == "__main__":
    # 使用 webview 打开 FastAPI
    window = webview.create_window(
        title='Yanx',
        url=f"http://localhost:{port}/",
        width=720,
        height=690,
        resizable=False,
        confirm_close=True,
        text_select=False,
    )

    window.events.closed += on_closed # 窗口关闭时退出程序
    webview.start(start_server)
