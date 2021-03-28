# coding:  utf8
import gzip
import json
import os.path
from pathlib import Path
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from requests import RequestException

from rtcookies import getcookie


def get_one_page(url_):
    headers_ = getcookie(url_)
    req = Request(url=url_, headers=headers_, method='POST')
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            return gzip.decompress(response.read()).decode('utf8')
    except RequestException:
        return None


def getexamscop(con):
    list6 = []
    for i in con[1]:
        url = i
        soup = BeautifulSoup(get_one_page(url_=url), 'html.parser')
        qq = soup.find(class_='zsml-wrapper')
        major_info = qq.find(class_='zsml-condition').select('tbody')[0]  # 专业信息
        thd = ['招生单位', '考试方式', '院系所', '跨专业', '专业', '学习方式', '研究方向', '指导老师', '拟招人数', '备注']
        thc = [u.text for u in qq.find_all('td', class_='zsml-summary')]
        thc.append(major_info.find_all(class_='zsml-bz')[-1].text)
        thee = dict(zip(thd, thc))
        exam_scope = qq.find(class_='zsml-result')  # 考试范围
        zsmlitems = [BeautifulSoup(str(u), 'lxml').find('td').find(text=True).strip() for u in
                     exam_scope.select('tbody')[0].select('td')]
        zsmls = [u.find(class_='sub-msg').text for u in exam_scope.select('tbody')[0].select('td')]
        thee['考试科目'] = dict(zip(zsmlitems, zsmls))
        list6.append(thee)

    return {con[0]: list6}


if __name__ == '__main__':
    udict = {}
    u_list = []
    for filename in os.listdir("university_majors/"):
        u_list.append('{}'.format(filename[:-5]))
    for filename in u_list:
        with open('university_majors/{}.json'.format(filename), 'r', encoding='utf8') as f:
            load_dict = json.load(f)
        udict[filename] = [u['考试范围'] for u in load_dict[filename]]
    # 写文件
    with open('university_majors_url/umu.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(udict, ensure_ascii=False) + '\n')
    # 读文件
    with open('university_majors_url/umu.json', 'r', encoding='utf8') as f:
        u_url = json.load(f)

    listqu = []
    num = len(u_url)
    num1 = 0
    for i in u_url.items():
        num1 += 1
        my_file = Path('college_majors_exam_scope/{}.json'.format(i[0]))
        if my_file.exists():
            continue
        else:
            print('第{}个 {}  进度{:.2}%'.format(num1, i[0], (num1 / num)*100))
            # 写文件
            mydict = getexamscop(i)
            with open('college_majors_exam_scope/{}.json'.format(i[0]), 'w', encoding='utf-8') as f:
                f.write(json.dumps(mydict, ensure_ascii=False) + '\n')
