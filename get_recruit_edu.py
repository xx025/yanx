import re

from bs4 import BeautifulSoup

from con_db import cur, con
from requests_ import req_post


class get_zsyx:
    def __init__(self, mldm: str, yjxkm: str, ssdm='', dwmc='', mlmc='', zymc='', xxfs=''):
        self.url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
        self.__data = []
        cur.execute('DELETE FROM tmpzhaoshengdanwei')
        self.__req_data = {'ssdm': ssdm,
                           'dwmc': dwmc,
                           'mldm': mldm,
                           'mlmc': mlmc,
                           'yjxkdm': yjxkm,
                           'zymc': zymc,
                           'xxfs': xxfs}

    def req_data(self):
        while True:
            page_text = req_post(url=self.url, data=self.__req_data)

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

            soup = BeautifulSoup(page_text)
            list = soup.select(".ch-table tbody tr")

            for i in list:
                url = i.select_one('td form a').get('href')
                zsdw = i.select_one('td form a').text
                local = i.select('td')[1].text
                yjsy = i.select('td')[2].select('i').__len__()
                zzhxyx = i.select('td')[3].select('i').__len__()
                bsd = i.select('td')[4].select('i').__len__()

                lds = (zsdw, local, yjsy, zzhxyx, bsd, url)
                self.__data.append(lds)

            if 'lip-input-box' in soup.select_one('.lip-last').get('class'):
                # 页面较多取倒数第二个
                next_page = soup.select('.lip')[soup.select('.lip').__len__() - 2]
            else:
                next_page = soup.select('.lip')[soup.select('.lip').__len__() - 1]

            if 'unable' in next_page.get('class'):
                break
            else:
                next_page = next_page.select_one('a').get('onclick')
                page_next = re.findall(r"[(](.*?)[)]", next_page)[-1]
                self.__req_data['pageno'] = page_next
                print('下一页' + page_next)

        self.__store_in_db()

    def __store_in_db(self):
        cur.execute('DELETE FROM tmpzhaoshengdanwei')
        cur.executemany('INSERT INTO tmpzhaoshengdanwei (zsdw, local, yjsy, zzhxyx, bsd, url)'
                        ' VALUES (?,?,?,?,?,?)', self.__data)
        con.commit()

    def get_data(self):
        cursor = cur.execute("SELECT *  FROM tmpzhaoshengdanwei")
        data = [i for i in cursor]
        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data
