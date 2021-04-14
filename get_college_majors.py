# coding:  utf8
import json
import re
from urllib import parse, request

from bs4 import BeautifulSoup
from requests import RequestException

from uinnfo.loc_ab_uni_985211 import list211

'''
此脚本是为了获取某个学校某类专业目录

'''
url = 'https://yz.chsi.com.cn/zsml/querySchAction.do'


# url = quote(url, safe=string.printable)#进行参数转换
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
def getInfoExame(schoolName, formdata):
    nextPage = 1
    thead = ['考试方式', '院系所', '专业', '研究方向', '学习方式', '指导教师', '拟招生人数', '考试范围', '跨专业', '备注']
    listU = []
    while True:
        formdata['pageno']= nextPage
        soup = BeautifulSoup(post_url(formdata), 'html.parser')
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


def getN(shN, formdata):
    with open('university_majors/{}/{}.json'.format(formdata['mldm'],shN), 'w', encoding='utf-8') as f:
        f.write(json.dumps(getInfoExame(schoolName=shN, formdata=formdata), ensure_ascii=False) + '\n')


if __name__ == '__main__':
    yjxkdm = '0812'
    zymc = ''
    mldm= '08'
    for i in list211:
        print(i)
        formdata = {'ssdm': '',
                    'dwmc': i,
                    'mldm': mldm,
                    'mlmc': '',
                    'yjxkdm': yjxkdm,
                    'zymc': zymc,
                    'xxfs': ''}
        getN(i, formdata=formdata)

'''
学术学位
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
'''
专业学位
ssdm: 
dwmc: 
mldm: zyxw
mlmc: 
yjxkdm: 0854
zymc: 电子信息
xxfs: 

'''
