import requests
from bs4 import BeautifulSoup

from processing_string import get_url_param
from processing_string.print_string import print_t
from download_university_info.yzw_pages import yzw_table


class dl_majors:
    def __init__(self):
        self.__rules = None
        self.__data = []
        self.__urls = []

    def set_rules(self, rules, con, cur):
        self.__rules = rules
        self.__set_urls(con, cur)

    def __set_urls(self, con, cur):

        t_data = [i[1] for i in self.__rules.items()]
        cons = cur.execute(
            '''SELECT * from 招生院校索引 where 招生院校索引.dwmc in (SELECT 院校名称 from 院校库 where 院校库.IS211 >= ? and 院校库.IS985 >= ? and 院校库.双一流 >= ?)''',
            t_data)
        for ks in cons:
            u = 'https://yz.chsi.com.cn/zsml/querySchAction.do?ssdm={}&dwmc={}&mldm={}&mlmc={}&yjxkdm={}&xxfs={}&zymc={}'.format(
                ks[0], ks[1], ks[2], ks[3], ks[4], ks[5], ks[6])
            self.__urls.append(u)

    def dl_data(self, con, cur):
        count: int = len(self.__urls)
        for i in range(count):
            tmp_data = self.__req_data_on_page(url=self.__urls[i])
            print_t(f'正在下载招专业信息:[{i + 1}/{count}]')
            self.__data.extend(tmp_data)
        self.__store_in_db(con, cur)

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
                ksfw = get_url_param(k.select('td')[7].select_one('a').get('href')).get('id')

                result_list.append((ksfw,))

            max_page = yzw_table.get_max_page(soup) if max_page is None else max_page

            now_page = yzw_table.get_now_page(soup)

            print_t('共{}页，当前第{}页'.format(max_page, now_page))
            if now_page == max_page:
                break
            else:
                next_page = 1 + now_page
                url = next_page_url + str(next_page)
        return result_list

    def __store_in_db(self, con, cur):

        cur.executemany(
            'INSERT INTO 招生专业索引(ID)VALUES (?)', self.__data)
        con.commit()
