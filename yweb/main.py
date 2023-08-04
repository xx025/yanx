import asyncio

from fastapi import APIRouter, HTTPException
from fastapi import Depends, Request
from requests_enhance import req_json_by_post
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketState
from yzw_dl import dl_zsyx, dl_yxzy, dl_ksfw
from yzw_dl.tools import parse_config, output_csvfile

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


# 定义一个依赖项函数，用于获取请求对象
def get_request(request: Request = Depends()):
    return request


@yanx_app.websocket("/wsdl")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        dlparams = ws.session.get('dlparams', {})  # 从 Session 中获取下载参数
        # tag: 原来向办法通过传递一个 request 对象来获取 Session,问了chatgpt好久也没说明白
        # 调试后发现，ws 对象中已经包含了 request 对象的session属性，所以直接使用即可
        # {'mllb': 'zyxw', 'xklb': '0101', 'zymc': '', 'xxfs': '', 'yxjh': '', 'yxdq': ''}
        if not dlparams:
            raise HTTPException(status_code=400, detail="No download parameters found")
        # dlparams 和 yzw-dl  的 config_values 不一致，需要转换一下
        config_values = {}
        config_values['ssdm'] = ''  # 省市代码
        config_values['dwmc'] = ''  # 单位名称
        config_values['mldm'] = dlparams.get('mllb', '')  # 门类类别
        config_values['yjxkdm'] = dlparams.get('xklb', '')  # 学科类别
        config_values['zymc'] = dlparams.get('zymc', '')  # 专业名称
        config_values['xxfs'] = dlparams.get('xxfs', '')  # 学习方式

        param_list = parse_config(config_values)  # 解析后的参数列表
        Dl_Data = {}

        # 构造进度信息的初始状态
        progress_data = {
            "院校信息": 0,
            "专业信息": 0,
            "考试信息": 0
        }

        for i_ in range(len(param_list)):
            _param = param_list[i_]
            for sch in dl_zsyx(**_param):
                Dl_Data[sch.招生单位] = sch.dict()
                progress_data["院校信息"] = int((i_ + 1) / len(param_list) * 100)
                await ws.send_json(progress_data)
        else:
            # 院校信息下载完成后，开始下载专业信息
            Dl_Data_keys = list(Dl_Data.keys())
            for j_ in range(len(Dl_Data_keys)):
                key = Dl_Data_keys[j_]
                param = Dl_Data[key]['dl_params']
                Dl_Data[key]['招生专业'] = {zs.id: zs.dict() for zs in dl_yxzy(**param)}
                progress_data["专业信息"] = int((j_ + 1) / len(Dl_Data_keys) * 100)
                await ws.send_json(progress_data)
            else:
                for k_ in range(len(Dl_Data_keys)):
                    key = Dl_Data_keys[k_]
                    for zyid in Dl_Data[key]['招生专业'].keys():
                        my_dl_ksfw = dl_ksfw(zyid)
                        zsml = my_dl_ksfw['zsml'].dict()  # 在详情页面会有一些更详细的信息
                        ksfw = [ks_.dict() for ks_ in my_dl_ksfw['ksfw']]  # 考试科目范围
                        dict1 = Dl_Data[key]['招生专业'][zyid]
                        dict1.update(zsml)  # 更新招生专业信息
                        dict1['考试范围'] = ksfw  # 添加考试科目范围
                        Dl_Data[key]['招生专业'][zyid] = dict1  # 更新招生专业信息
                    else:
                        progress_data["考试信息"] = int((k_ + 1) / len(Dl_Data_keys) * 100)
                        await ws.send_json(progress_data)
                else:
                    # 发送初始进度信息给前端
                    await ws.send_json(progress_data)
                    csv_title = [
                        "id",
                        "招生单位",
                        "所在地",
                        "院系所",
                        "专业",
                        '学习方式',
                        "研究方向",
                        "拟招人数",
                        "政治",
                        "外语",
                        "业务课一",
                        "业务课二",
                        "考试方式",
                        "指导老师",
                        '备注'
                    ]
                    # 保存数据到数据库
                    output_csvfile(Dl_Data, 'data.csv',csv_title)
        # 发送下载结束标识给前端
        await ws.send_json({"download_finished": True})
    except Exception as e:
        if ws.state == WebSocketState.CONNECTED:
            await ws.send_text(f"An error occurred: {str(e)}")
        else:
            # 抛出一场
            raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    finally:
        await ws.close()
