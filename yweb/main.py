from fastapi import APIRouter, Depends
from pydantic import BaseModel
from requests_enhance import req_json_by_post
from sqlalchemy.orm import Session

from database import get_db

yanx_app = APIRouter()


@yanx_app.get("/main_data")
async def main_data():
    data = {'title': 'YanX-研招网硕士专业目录下载',
            'describe': 'YanX是一个一键下载研招网专业目录的工具',
            'issue_url': 'https://github.com/xx025/yanx/issues',
            'gh_url': 'https://github.com/xx025'}
    return data


@yanx_app.get('/mldm')
async def get_mldm():
    """
    获取学科类别
    """
    url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'
    json_data = req_json_by_post(url=url)
    new_list = [{'label': f"{item['dm']}-{item['mc']}", 'value': item['dm']} for item in json_data]
    groups = [
        {
            'label': '专业学位',
            'options': [{'label': '专业学位', 'value': 'zyxw'}]
        }, {
            'label': '学术学位',
            'options': new_list
        }
    ]
    return groups


@yanx_app.get('/xklb')
async def get_xklb(mldm: str):
    """
    获取学科类别
    允许有一个 mldm 标识门类代码
    """
    data = []
    try:
        url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
        json_data = req_json_by_post(url=url, data={'mldm': mldm})
        data = [{'label': f"{item['dm']}-{item['mc']}", 'value': item['dm']} for item in json_data]

    finally:
        return data


@yanx_app.get('/zymc')
async def get_zymc(dm: str):
    """
    获取专业名称
    允许有一个 mldm 标识门类代码
    """

    data = []
    try:
        url = 'https://yz.chsi.com.cn/zsml/code/zy.do'
        data = req_json_by_post(url=url, data={'q': dm})
    finally:
        return data


@yanx_app.get('/dl_data')
async def dl_data(db: Session = Depends(get_db)):
    # tasks = db.query(Download).filter(Download.available == 1).all()
    # 数据库中已下载的任务
    tasks = [
        [1, 1]
    ]
    return [{'id': i[0], 'name': i[1]} for i in tasks]


@yanx_app.get('/open_link')
async def open_link(url: str):
    """
    通过外部浏览器打开链接
    """
    import webbrowser
    webbrowser.open_new_tab(url)
    return {"message": f"已打开链接{url}"}


class DlParams(BaseModel):
    mllb: str  # 门类类别，如专硕和学硕
    xklb: str  # 学科类别，如哲学和经济学
    zymc: str  # 专业名称
    xxfs: str  # 学习方式
    yxjh: str  # 院校建设计划，如985、211
    yxdq: str  # 院校地区， 如A区和B区


@yanx_app.post('/new_dl')
async def new_dl(params: DlParams):
    return {'message': '创建成功'}


@yanx_app.post("/stop_download")
async def stop_download():
    return {"message": "下载进程已停止"}


@yanx_app.get('/progress')
async def get_progress():
    return {'message': '获取进度'}
