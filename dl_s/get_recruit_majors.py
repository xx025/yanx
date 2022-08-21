import requests
from bs4 import BeautifulSoup

from db import cur, con
from user.yzw_pages import yzw_table


class dl_majors:
    def __init__(self):
        self.__rules = None
        self.__data = []
        self.__urls = None

    def set_rules(self, rules):
        self.__rules = rules
        self.__set_urls()

    def __set_urls(self):

        t_data = [i[1] for i in self.__rules.items()]
        cons = cur.execute(
            "SELECT recruit_school.url from recruit_school where recruit_school.zsdw "
            "in (SELECT name from edus  where edus.is211 >= ? and edus.is985 >= ? and edus.is11 >= ?)",
            t_data)
        self.__urls = [i[0] for i in cons]

    def dl_data(self):
        count: int = len(self.__urls)
        for i in range(count):
            tmp_data = self.__req_data_on_page(url=self.__urls[i])
            for k in tmp_data:
                print(k)
            print(f'正在下载招专业信息:[{i + 1}/{count}]')
            self.__data.extend(tmp_data)
        self.__store_in_db()

        return self.__data

    @staticmethod
    def __req_data_on_page(url):
        next_page_url = url + '&pageno='
        result_list = []
        max_page = None
        while True:
            page = requests.get(url=url)
            page_text = page.text
            soup = BeautifulSoup(page_text, 'html.parser')
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
                lrd = (url, ksfs, yxs, zy, yjfx, xxfs, zdls, zsrs, ksfw, bz)
                result_list.append(lrd)

            max_page = yzw_table.get_max_page(soup) if max_page is None else max_page

            now_page = yzw_table.get_now_page(soup)

            print('共{}页，当前第{}页'.format(max_page, now_page))
            if now_page == max_page:
                break
            else:
                next_page = 1 + now_page
                url = next_page_url + str(next_page)
        return result_list

    def __store_in_db(self):

        cur.executemany(
            'INSERT INTO recruit_major(yxlj, ksfs, yxs, zy, yjfx, xxfs, zdls, zsrs, ksfw, bz)'
            'VALUES (?,?,?,?,?,?,?,?,?,?)', self.__data)
        con.commit()