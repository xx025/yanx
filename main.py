import gzip
import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from requests import RequestException

rel= []


A = ['北京', '天津', '河北', '山西', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '重庆',
     '四川', '陕西']

B = ['内蒙古', '广西', '海南', '贵州', '云南', '西藏', '甘肃', '青海', '宁夏', '新疆']

list985 = ['北京大学', '中国人民大学', '清华大学', '北京航空航天大学', '北京理工大学', '中国农业大学', '北京师范大学', '中央民族大学', '南开大学', '天津大学', '大连理工大学',
           '东北大学', '吉林大学', '哈尔滨工业大学', '复旦大学', '同济大学', '上海交通大学', '华东师范大学', '南京大学', '东南大学', '浙江大学', '中国科学技术大学', '厦门大学',
           '山东大学', '中国海洋大学', '武汉大学', '华中科技大学', '湖南大学', '中南大学', '国防科学技术大学', '中山大学', '华南理工大学', '四川大学', '电子科技大学', '重庆大学',
           '西安交通大学', '西北工业大学', '西北农林科技大学', '兰州大学']

list211 = ['北京大学', '中国人民大学', '清华大学', '北京交通大学', '北京工业大学', '北京航空航天大学', '北京理工大学', '北京科技大学', '北京化工大学', '北京邮电大学', '中国农业大学',
           '北京林业大学', '北京中医药大学', '北京师范大学', '北京外国语大学', '中国传媒大学', '中央财经大学', '对外经济贸易大学', '北京体育大学', '中央音乐学院', '中央民族大学',
           '中国政法大学', '华北电力大学', '南开大学', '天津大学', '天津医科大学', '河北工业大学', '太原理工大学', '内蒙古大学', '辽宁大学', '大连理工大学', '东北大学',
           '大连海事大学', '吉林大学', '延边大学', '东北师范大学', '哈尔滨工业大学', '哈尔滨工程大学', '东北农业大学', '东北林业大学', '复旦大学', '同济大学', '上海交通大学',
           '华东理工大学', '东华大学', '华东师范大学', '上海外国语大学', '上海财经大学', '上海大学', '第二军医大学 ', '南京大学', '苏州大学', '东南大学', '南京航空航天大学',
           '南京理工大学', '中国矿业大学', '河海大学', '江南大学', '南京农业大学', '中国药科大学', '南京师范大学', '浙江大学', '安徽大学', '中国科学技术大学', '合肥工业大学',
           '厦门大学', '福州大学', '南昌大学', '山东大学', '中国海洋大学', '中国石油大学', '郑州大学', '武汉大学', '华中科技大学', '中国地质大学', '武汉理工大学', '华中农业大学',
           '华中师范大学', '中南财经政法大学', '湖南大学', '中南大学', '湖南师范大学', '国防科学技术大学', '中山大学', '暨南大学', '华南理工大学', '华南师范大学', '广西大学',
           '海南大学', '四川大学', '西南交通大学', '电子科技大学', '四川农业大学', '西南财经大学', '重庆大学', '西南大学', '贵州大学', '云南大学', '西藏大学', '西北大学',
           '西安交通大学', '西北工业大学', '西安电子科技大学', '长安大学', '西北农林科技大学', '陕西师范大学', '第四军医大学', '兰州大学', '青海大学', '宁夏大学', '新疆大学',
           '石河子大学']

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
    for i in result[1:]:
        th = ['计划', 'AB区', '院校名称', '所在地', '院校隶属', '研究生院', '自划线院校',
              '网报公告', '招生简章', '在线咨询', '调剂办法']
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


resultd={'data':rel}

with open('edudata.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(resultd, ensure_ascii=False) + '\n')