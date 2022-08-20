from bs4 import BeautifulSoup

from con_db import cur, con
from edu985211list import loc_B, loc_A, list211, list985
from requests_ import req_method


class edu:
    def __init__(self, name, is11, loc, lishu, yjsy, zzhx):
        self.name = name
        self.is11 = is11
        self.is985 = 1 if name in list985 else 0
        self.is211 = 1 if name in list211 else 0
        self.locAB = 'B' if loc in loc_B else 'A'
        self.loc = loc
        self.lishu = lishu
        self.yjsy = yjsy
        self.zzhx = zzhx

    def info(self):
        return (self.name,
                self.is11,
                self.is985,
                self.is211,
                self.locAB,
                self.loc,
                self.lishu,
                self.yjsy,
                self.zzhx)


class get_edus:
    def __init__(self):
        self.url = 'https://yz.chsi.com.cn/sch/'
        self.data = []
        self.l_B = loc_B
        self.l_A = loc_A
        self.list211 = list211
        self.list985 = list985
        self.start = 0

    def __req_data(self):
        while True:
            page_text = req_method(url=self.url, method='get', params={'start': self.start})
            soup = BeautifulSoup(page_text)
            if soup.select('.yxk-table table tbody tr').__len__() == 1 and soup.select_one(
                    '.yxk-table table .noResult'):
                break
            else:
                self.start += 20
                print('下一页')
            for i in soup.select('.yxk-table table tbody tr'):
                name = i.select('td')[0].select_one('a').text.strip()
                is11 = 1 if i.select('td')[0].select_one('span') else 0
                loc = i.select('td')[1].text
                lishu = i.select('td')[2].text
                yjsy = 1 if i.select('td')[3].select_one('i') is None else 0
                zzhx = 1 if i.select('td')[4].select_one('i') is None else 0

                newedu = edu(name=name,
                             is11=is11,
                             loc=loc,
                             lishu=lishu,
                             yjsy=yjsy,
                             zzhx=zzhx)
                self.data.append(newedu.info())
        self.__store_in_db()

    def __store_in_db(self):
        cur.execute('DELETE FROM edus')
        cur.executemany(
            'INSERT INTO edus(name, is11, is985, is211,locAB, loc, lishu, yjsy, zzhx)'
            'VALUES (?,?,?,?,?,?,?,?,?)', self.data)
        con.commit()

    def get_data(self):
        cursor = cur.execute("SELECT *  FROM edus")
        data = [i for i in cursor]
        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data


cur.execute('DELETE FROM edus')
ge2 = get_edus()
ge2.get_data()
