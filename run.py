import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from flaskwebgui import FlaskUI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from yweb import yanx_app as yanx_app

app = FastAPI()

# 添加 session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.include_router(yanx_app, prefix='/api')

# Mounting default static files
app.mount(path="/static", app=StaticFiles(directory="./static"), name="static")

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


@app.get("/dl", response_class=HTMLResponse)
async def root2(request: Request):
    return templates.TemplateResponse("download.html", {"request": request, 'title': 'YanX-研招网硕士专业目录下载'})


if __name__ == "__main__":
    uvicorn.run('run:app', host='localhost', reload=True, port=5511)

    # FlaskUI(app=app, server="fastapi",
    #         width=720,
    #         height=680,
    #         ).run()
