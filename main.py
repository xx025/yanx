'''
此脚本爬取学校目录并输出到edudata.json文件
'''

import gzip
import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from requests import RequestException

from uinnfo.loc_ab_uni_985211 import list211, list985, A, B

rel = []

Headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Referer': 'https://yz.chsi.com.cn/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4449.6 Safari/537.36'}


def getUnt(HTML):
    soup = BeautifulSoup(HTML, "lxml")  # 格式化
    result = soup.select("div tr")
    th = ['计划', 'AB区', '院校名称', '所在地', '院校隶属', '研究生院', '自划线院校',
          '网报公告', '招生简章', '在线咨询', '调剂办法']
    for i in result[1:]:
        kd = [u for u in i.find_all("td")]
        kd1 = [u.text.replace('\n', '').replace('\r', '').replace(' ', '') for u in kd[0:3]]
        kd0 = kd1[0:2]
        if kd0[0] in list211 and kd0[0] in list985:
            kd0[0] = "985&211"
        elif kd0[0] in list985:
            kd0[0] = "985"
        elif kd0[0] in list211:
            kd0[0] = "211"
        else:
            kd0[0] = ""

        if kd0[1] in A:
            kd0[1] = "A"
        elif kd0[1] in B:
            kd0[1] = "B"
        else:
            continue

        kd2 = [u for u in kd[3:5]]
        for j in range(2):
            if kd2[j].find('i', class_="iconfont ch-table-tick"):
                kd2[j] = True
            else:
                kd2[j] = False

        kd3 = ['https://yz.chsi.com.cn/' + u.find_all("a")[0].get('href') for u in kd[5:]]

        kdic = dict(zip(th, kd0 + kd1 + kd2 + kd3))
        rel.append(kdic)
        print(kdic)


def get_one_page(url_, headers_):
    req = Request(url=url_, headers=headers_, method='POST')
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            return gzip.decompress(response.read()).decode('utf8')
    except RequestException:
        return None


pages = 0

while (True):
    url = 'https://yz.chsi.com.cn/sch/?start={}'.format(pages)
    getUnt(get_one_page(url_=url, headers_=Headers))
    pages += 20
    if pages >= 860:
        break
print(rel)

resultd = {'data': rel}

with open('uinnfo/edudata.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(resultd, ensure_ascii=False) + '\n')
