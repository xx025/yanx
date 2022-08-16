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

    # def req_data(self):
    #     def req_data(self):
    #         while True:
    #             page_text = req_method(url=self.url, method='get', params={'start': '20'})
    #             soup = BeautifulSoup(page_text)
    # list = soup.select(".ch-table tbody tr")

    #         for i in list:
    #             url = i.select_one('td form a').get('href')
    #             zsdw = i.select_one('td form a').text
    #             local = i.select('td')[1].text
    #             yjsy = i.select('td')[2].select('i').__len__()
    #             zzhxyx = i.select('td')[3].select('i').__len__()
    #             bsd = i.select('td')[4].select('i').__len__()
    #
    #             lds = (zsdw, local, yjsy, zzhxyx, bsd, url)
    #             self.__data.append(lds)
    #
    #         if 'lip-input-box' in soup.select_one('.lip-last').get('class'):
    #             # 页面较多取倒数第二个
    #             next_page = soup.select('.lip')[soup.select('.lip').__len__() - 2]
    #         else:
    #             next_page = soup.select('.lip')[soup.select('.lip').__len__() - 1]
    #
    #         if 'unable' in next_page.get('class'):
    #             break
    #         else:
    #             next_page = next_page.select_one('a').get('onclick')
    #             page_next = re.findall(r"[(](.*?)[)]", next_page)[-1]
    #             self.__req_data['pageno'] = page_next
    #             print('下一页' + page_next)
    #
    #     self.__store_in_db()
    #
    # def __store_in_db(self):
    #     cur.execute('DELETE FROM zhaoshengyuanxiao')
    #     cur.executemany('INSERT INTO zhaoshengyuanxiao (zsdw, local, yjsy, zzhxyx, bsd, url)'
    #                     ' VALUES (?,?,?,?,?,?)', self.__data)
    #     con.commit()
    #
    # def get_data(self):
    #     cursor = cur.execute("SELECT *  FROM zhaoshengyuanxiao")
    #     data = [i for i in cursor]
    #     if len(data) == 0:
    #         self.__req_data()
    #         return self.get_data()
    #     else:
    #         return data
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
                print(newedu.info())
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
new_get_edus = get_edus()
new_get_edus.get_data()
