import asyncio
import json
import os

from fastapi import APIRouter, HTTPException
from fastapi import Request
from requests_enhance import req_json_by_post, req_json_by_get
from starlette.background import BackgroundTask
from starlette.responses import FileResponse
from starlette.websockets import WebSocket, WebSocketState

from yweb.tools import create_file_name
from yweb.yzw_down import DownTask
from yzw_dl.tools import output_csvfile

yanx_app = APIRouter()


@yanx_app.get("/main_data")
async def main_data():
    data = {'title': 'YanX-研招网硕士专业目录下载',
            'describe': 'YanX是一个一键下载研招网专业目录的工具',
            'issue_url': 'https://github.com/xx025/yanx/issues',
            'gh_url': 'https://github.com/xx025'}
    return data


@yanx_app.get('/mldm')
async def get_mldm(request: Request):
    """
    获取学科类别
    """
    url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'
    json_data = req_json_by_post(url=url)
    new_list = [{'label': f"{item['dm']}-{item['mc']}", 'value': item['dm']} for item in json_data]
    groups = [
        {
            'label': '专业学位', 'options': [{'label': '专业学位', 'value': 'zyxw'}]
        }, {
            'label': '学术学位', 'options': new_list
        }
    ]

    if request.session.get('mldm') is None:
        request.session['mldm'] = {}

    tmp_dict = request.session['mldm']
    tmp_dict.update({'zyxw': '专业学位'})
    tmp_dict.update({item['dm']: item['mc'] for item in json_data})
    request.session['mldm'] = tmp_dict

    return groups


@yanx_app.get('/xklb')
async def get_xklb(mldm: str, request: Request):
    """
    获取学科类别
    允许有一个 mldm 标识门类代码
    """
    data = []
    json_data = []
    try:
        url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
        json_data = req_json_by_get(url=url, params={'mldm': mldm})
        data = [{'label': f"{item['dm']}-{item['mc']}", 'value': item['dm']} for item in json_data]

    finally:
        if request.session.get('xklb') is None:
            request.session['xklb'] = {}
        tmp_dict = request.session['xklb']
        tmp_dict.update({item['dm']: item['mc'] for item in json_data})
        request.session['xklb'] = tmp_dict
        return data


@yanx_app.get('/zymc')
async def get_zymc(dm: str, request: Request):
    """
    获取专业名称
    允许有一个 mldm 标识门类代码
    """
    data = []
    try:
        url = 'https://yz.chsi.com.cn/zsml/code/zy.do'
        data = req_json_by_get(url=url, params={'q': dm})
    finally:
        return data


@yanx_app.get('/dl_data')
async def dl_data():
    # 不用数据库
    tasks = [
        [1, 1]
    ]
    return [{'id': i[0], 'name': i[1]} for i in tasks]


g_save_name = ''


@yanx_app.websocket("/wsdl")
async def websocket_endpoint(ws: WebSocket):
    # 将新连接添加到活动连接集合
    await ws.accept()
    dlparams = ws.session.get('dlparams')
    save_name = create_file_name(dlparams, ws.session)
    dlth = DownTask(dlparams, save_name)
    global g_save_name
    g_save_name = save_name
    try:
        async def receive_messages():
            while True:
                data = await ws.receive_text()
                print(f"Received message: {data}")
                if data == 'close':
                    dlth.stop()  # 停止下载
                    await ws.close()

        async def start_download():
            dlth.start()
            while True:
                if dlth.is_alive():
                    await asyncio.sleep(1)
                    progress_data = dlth.get_dl_progress()
                    await ws.send_json(progress_data)
                    if all([i == 100 for i in progress_data.values()]):
                        await ws.send_json({'downloadFinished': True})
                        dlth.stop()
                        break

        await asyncio.gather(receive_messages(), start_download())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    finally:
        if ws.state == WebSocketState.CONNECTED:
            if dlth.is_alive():
                dlth.stop()
            await ws.close()


@yanx_app.get("/out_to_csv")
async def out_to_csv():
    save_name = g_save_name
    out_json_path = os.path.join('static/dldocs', f'{save_name}.json')
    out_csv_path = os.path.join('static/dldocs', f'{save_name}.csv')
    csv_title = ["id", "招生单位", "所在地", "院系所", "专业", '学习方式', "研究方向", "拟招人数", "政治",
                 "外语", "业务课一", "业务课二", "考试方式", "指导老师", '备注']

    with open(out_json_path, 'r', encoding='utf-8') as f:
        Dl_Data = json.load(f)  # 保存为CSV文件
        output_csvfile(data=Dl_Data, file_name=out_csv_path, title=csv_title)
    return FileResponse(out_csv_path,
                        filename=f'{save_name}.csv',
                        background=BackgroundTask(lambda: os.remove(out_csv_path)))
