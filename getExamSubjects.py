#!/usr/bin/python3
# coding:  utf8
# @File    : getExamSubjects.py
# @author  :xx025

import json
import re
from urllib import parse, request

from bs4 import BeautifulSoup
from requests import RequestException

'''
此脚本是为了获取某个学校某个专业的考试科目

'''
#
# headers = {
#     'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Encoding': ' gzip, deflate, br',
#     'Accept-Language': ' zh-CN,zh;q=0.9',
#     'Cache-Control': ' max-age=0',
#     'Connection': ' keep-alive',
#     'Cookie': ' JSESSIONID=2EF609D5223C12FD32C030D6DF997F3C; zg_did=%7B%22did%22%3A%20%22178685f48124b-0dea03d8ab43ec-6252732d-144000-178685f481317%22%7D; aliyungf_tc=e6118c040f377c26fcd0cb97709daa2bcf32666b377bc53b8708409b59ab8b06; JSESSIONID=E1E823F4CCBFC65AD9C54B347E4045F0; XSRF-CCKTOKEN=33d68cd8d8e5c30816b1b4eb22784ca2; CHSICC_CLIENTFLAGYZ=e839bc16219ba5185d0ac62e0e39117d; CHSICC_CLIENTFLAGZSML=1f7c0048e2a49f1501a5e6658c46b4ea; acw_tc=781bad1016168517402707695e0d39f81aa0dbb02b43997ca7510949182552; zg_adfb574f9c54457db21741353c3b0aa7=%7B%22sid%22%3A%201616850032025%2C%22updated%22%3A%201616853092929%2C%22info%22%3A%201616658778142%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fyz.chsi.com.cn%2F%22%7D',
#     'DNT': ' 1',
#     'Host': ' yz.chsi.com.cn',
#     'sec-ch-ua': ' " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
#     'sec-ch-ua-mobile': ' ?0',
#     'Sec-Fetch-Dest': ' document',
#     'Sec-Fetch-Mode': ' navigate',
#     'Sec-Fetch-Site': ' none',
#     'Sec-Fetch-User': ' ?1',
#     'Upgrade-Insecure-Requests': ' 1',
#     'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4449.6 Safari/537.36'
# }


# def get_one_page(url_, headers_):
#     req = Request(url=url_, headers=headers_, method='POST')
#     try:
#         response = urlopen(req)
#         if response.getcode() == 200:
#             return gzip.decompress(response.read()).decode('utf8')
#     except RequestException:
#         return None

# url = quote(url, safe=string.printable)#进行参数转换


'''
参数含义：
ssdm:   省市         如：11
dwmc:   单位名称      如：北京大学
mldm:   学科门类      如：08
mlmc:  （我不知道）
yjxkdm: 学科类别      如：0812, 
zymc:   专业
xxfs:   学习方式
pageno： 页码         如： 1  在多页的情况下返回第一页
'''

# url = "https://yz.chsi.com.cn/zsml/queryAction.do"
# 查询页面
url = 'https://yz.chsi.com.cn/zsml/querySchAction.do'


def post_url(formData):
    data_parse = parse.urlencode(formData)
    data = data_parse.encode('utf-8')
    try:
        response = request.urlopen(url=url, data=data)
        if response.getcode() == 200:
            return response.read().decode('utf8')
    except RequestException:
        return None


# 查询的方式找到与参数对应的链接
def getInfoExame(schoolName):
    nextPage = 1
    thead = ['考试方式', '院系所', '专业', '研究方向', '学习方式', '指导教师', '拟招生人数', '考试范围', '跨专业', '备注']
    listU = []
    while True:
        formData = {'ssdm': '', 'dwmc': schoolName, 'mldm': '08', 'mlmc': '', 'yjxkdm': '0812', 'zymc': '', 'xxfs': '',
                    'pageno': nextPage}
        soup = BeautifulSoup(post_url(formData), 'html.parser')
        table = soup.find('table', class_='ch-table').find('tbody').find_all('tr')
        for i in table:
            kd = i.find_all('td')
            kd1 = [i.text.replace('\n', '').replace('\r', '').replace(' ', '') for i in kd[:6]]
            kd2 = str(kd[6].find('script')).replace('\n', '').replace('\r', '').replace(' ', '')
            kd2 = re.search(r"['](.*?)[']", kd2).groups()[0]  # 招生人数
            kd3 = ['https://yz.chsi.com.cn' + u.find('a').attrs['href'] for u in kd[7:9]]  # 考试范围,跨专业
            kd4 = str(kd[9].find('script')).replace('\n', '').replace('\r', '').replace(' ', '')
            kd4 = re.search(r"['](.*?)[']", kd4).groups()[0]  # 备注
            kd = kd1 + [kd2] + kd3 + [kd4]
            kdic = dict(zip(thead, kd))
            listU.append(kdic)
        nextPageTur = soup.find(class_='zsml-page-box').find(class_='lip-last')  # nextpage
        if 'unable' not in nextPageTur.attrs['class']:
            nextPage += 1
            print('继续下一页')
        else:
            print('最后一页结束')
            break  # 结束while循环
    return {schoolName: listU}


def getN(shN):
    with open('school_professional_directory/{}.json'.format(shN), 'w', encoding='utf-8') as f:
        f.write(json.dumps(getInfoExame(shN), ensure_ascii=False) + '\n')


getN('北京大学')