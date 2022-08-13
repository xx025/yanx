import re

import requests
from bs4 import BeautifulSoup

from con_db import cur, con

data = []

req_data = {'ssdm': '', 'dwmc': '', 'mldm': '05', 'mlmc': '', 'yjxkdm': '0501', 'zymc': '', 'xxfs': ''}
while True:

    try:
        print(req_data['pageno'])
    except:
        pass

    r = requests.post(url='https://yz.chsi.com.cn/zsml/queryAction.do', data=req_data)

    '''
    地区代码：'ssdm': '',
    单位名称  'dwmc': '',
    专业门类：'mldm': 'zyxw',
            'mlmc': '',
    专业代码：'yjxkdm': '0252',
    专业名称：'zymc': '',
    学习方式：'xxfs': ''
    页码： 'pageno': 3
    '''

    soup = BeautifulSoup(r.text)
    list = soup.select(".ch-table tbody tr")

    for i in list:
        url = i.select_one('td form a').get('href')
        zsdw = i.select_one('td form a').text
        local = i.select('td')[1].text
        yjsy = i.select('td')[2].select('i').__len__()
        zzhxyx = i.select('td')[3].select('i').__len__()
        bsd = i.select('td')[4].select('i').__len__()

        obnes = (zsdw, local, yjsy, zzhxyx, bsd, url)
        data.append(obnes)
        print(obnes)
    else:
        next_page = None

        if 'lip-input-box' in soup.select_one('.lip-last').get('class'):
            # 页面较多取倒数第二个
            next_page = soup.select('.lip')[soup.select('.lip').__len__() - 2]

        else:
            next_page = soup.select('.lip')[soup.select('.lip').__len__() - 1]

        if 'unable' in next_page.get('class'):
            print('结束，写入数据库')
            break
        else:
            next_page = next_page.select_one('a').get('onclick')

            page_next = re.findall(r"[(](.*?)[)]", next_page)[-1]
            req_data['pageno'] = page_next
            print('下一页' + page_next)

cur.execute('DELETE FROM tmpzhaoshengdanwei')
cur.executemany('INSERT INTO tmpzhaoshengdanwei (zsdw, local, yjsy, zzhxyx, bsd, url)'
                ' VALUES (?,?,?,?,?,?)', data)
con.commit()

con.close()
