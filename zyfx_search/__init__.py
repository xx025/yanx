"""

模拟 2023年硕士专业目录查询
https://yz.chsi.com.cn/zsml/zyfx_search.jsp

"""
import json

import stools

from db2 import get_dqdm
from stools.sk3 import req_get, req_post


# 设置一给全局查询字典

# 如果  界面上的文字 --> 真实的下载需要的参数


def get_yxqu_items():
    items = {'不做选择': None,
             'A区': 'a',
             'B区': 'b'
             }

    for dm, mc, ab in get_dqdm():
        key = f'{ab.upper()}{mc}'
        value = dm
        items[key] = value

    return items


g_params = {
    '学位类别': {
        'items': {'专业学位': '专业学位', '学术学位': '学术学位'},
        'selected': None
    },
    '门类类别': {
        'items': {},
        'selected': None
    },
    '学科类别': {
        'items': {},
        'selected': None
    },
    '专业名称': {
        'items': {},
        'selected': None
    },
    '学习方式': {
        'items': {'不做选择': '',
                  '全日制': '1',
                  '非全日制': '2'},
        'selected': None
    },
    '院校建设计划': {
        'items': {'不做选择': None,
                  '普通院校': '4',
                  '985院校': '985',
                  '211院校': '211',
                  '双一流院校': '11'},
        'selected': None
    },
    '院校区域': {
        'items': get_yxqu_items(),
        'selected': None
    }
}

# 1. 所在省市

pass


# 2.门类类别

class g_params_def:

    @staticmethod
    def update_mllb():

        selected = g_params['学位类别'].get('selected', None)

        if selected:
            if selected == '专业学位':
                g_params['门类类别']['items'] = {'专业学位': 'zyxw'}
            else:
                # 学术学位
                url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'
                json_data = json.loads(req_get(url).text)

                g_params['门类类别']['items'] = {}

                for k in json_data:
                    dm, mc = k['dm'], k['mc']
                    g_params['门类类别']['items'][f'{dm}-{mc}'] = dm

    @staticmethod
    def update_xklb():

        selected = g_params['门类类别'].get('selected', None)

        if selected:

            mldm = g_params['门类类别']['items'][selected]

            url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'

            r = req_post(url=url, data={'mldm': mldm}).text

            g_params['学科类别']['items'] = {}

            for k in json.loads(r):
                dm, mc = k['dm'], k['mc']
                g_params['学科类别']['items'][f'{dm}-{mc}'] = dm

    @staticmethod
    def update_zymc():

        selected = g_params['学科类别'].get('selected', None)

        if selected:
            url = 'https://yz.chsi.com.cn/zsml/code/zy.do'
            q = g_params['学科类别']['items'][selected]

            r = req_post(url=url, data={'q': q}).text
            req_data = json.loads(r)

            g_params['专业名称']['items'] = {}

            for item in req_data:
                g_params['专业名称']['items'][item] = item
