from bs4 import BeautifulSoup

from con_db import cur, con
from requests_ import req_method


class get_majors_of_edu:
    def __init__(self, url):
        self.url = url
        self.data = []

    def req_data(self):

        while True:
            page_text = req_method(url=self.url, method='get')
            soup = BeautifulSoup(page_text)

            for k in soup.select('.zsml-list-box tbody tr'):
                ksfs = k.select('td')[0].text
                yxs = k.select('td')[1].text
                zy = k.select('td')[2].text
                yjfx = k.select('td')[3].text
                xxfs = k.select('td')[4].text
                zdls = k.select('td')[5].text
                zsrs = k.select('td')[6].select_one('script').text
                ksfw = k.select('td')[7].select_one('a').get('href')
                bz = k.select('td')[8].text
                lrd = (self.url, ksfs, yxs, zy, yjfx, xxfs, zdls, zsrs, ksfw, bz)
                print(lrd[1:-1])
                self.data.append(lrd)
            if 'unable' in soup.select_one('.lip-last').get('class'):
                break
            else:
                print(self.url)
                print('存在下一页')
                break
        self.__store_in_db()

    def __store_in_db(self):

        cur.executemany(
            'INSERT INTO yuanxiaozhuanye(yxlj, ksfs, yxs, zy, yjfx, xxfs, zdls, zsrs, ksfw, bz)'
            'VALUES (?,?,?,?,?,?,?,?,?,?)', self.data)
        con.commit()
