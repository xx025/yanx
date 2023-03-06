import json
import re

import requests
from bs4 import BeautifulSoup

from utils.request_utils.rewirte_requests import req_get


def gta():
    try:
        url = 'https://gist.githubusercontent.com/xx025/a20824f364115bbc5f42ee340df6eaaa/raw'
        info = json.loads(requests.get(url, timeout=4).text)
    except Exception:

        GG = "这是一条公告\n BY:uir 或许由于github连接原因，你没有获取到最新公告，关注：https://xx025.github.io/YanX/ 获取最新动态"
        HY = '我是小萌！\\n\n请在Github帮小萌点亮Star吧，在下面\\n\n的输入框输入你的GitHub ID 就能使用了\\n\n~~~嘻嘻~~~\\n\n请不要滥用哦！！\n\n对了，点亮Star后 请等网络反应一会儿！\n\n小萌爱你哟！'

        info = {'update': {'local': True,
                           'update_mes': '当前版本已经发布30days,请检查新版本！'},
                'welcome_mes': {'title': '小萌来啦！',
                                'content': HY},
                'tips_mes': GG
                }
    return info


def get_year():
    try:
        url = 'https://yz.chsi.com.cn/zsml/zyfx_search.jsp'

        text = req_get(url=url).text
        soup = BeautifulSoup(text, 'html.parser')
        lt = soup.select_one('.zsml-form-box h2').text
        lt = re.findall("\d+", lt)[0]
        lt = int(lt)
    except:
        lt = None
    return lt
