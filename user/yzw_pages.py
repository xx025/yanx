import os
import re
from copy import copy

import requests
from bs4 import BeautifulSoup

from db import cur, con


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
            os.system('cls')
            print('正在下载招专业信息:[{}/{}]'.format(i + 1, count))
            self.__data.extend(self.__req_data_on_page(url=self.__urls[i]))
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


class dl_schools():
    def __init__(self):
        self.url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
        self.__data = []
        self.__datas_for_req_get = []

    def set_user_select_datas(self, choice_):
        datas_for_get = []
        use1_data = choice_
        xxfs = '' if not use1_data['learn_mode'] else use1_data['learn_mode']

        '''
         地区代码：'ssdm': '',
        单位名称  'dwmc': '',
        专业门类：'mldm': '02',
                'mlmc': '',
        专业代码：'yjxkdm': '0252',
        专业名称：'zymc': '',
        学习方式：'xxfs': ''
        页码： 'pageno': 3
        '''
        data1 = {'ssdm': '',
                 'dwmc': '',
                 'mldm': use1_data['discipline_code'],
                 'mlmc': '',
                 'yjxkdm': use1_data['field_of_study_code'],
                 'zymc': '',
                 'xxfs': xxfs
                 }

        locations = use1_data['location_codes']
        majors = use1_data['majors']

        if locations and majors:
            # 选择了多个地区 和专业
            for location_code in locations:
                for major_name in majors:
                    data2 = copy(data1)
                    data2['ssdm'] = location_code
                    data2['zymc'] = major_name
                    datas_for_get.append(data2)
        elif locations:
            # 仅选择了多个地区
            for location_code in locations:
                data2 = copy(data1)
                data2['ssdm'] = location_code
                datas_for_get.append(data2)
        elif majors:
            # 选择了多个专业
            for major_name in majors:
                data2 = copy(data1)
                data2['zymc'] = major_name
                datas_for_get.append(data2)
        else:
            # 地区和专业都没具体选择
            datas_for_get.append(data1)

        self.__datas_for_req_get = datas_for_get

    def dl_data(self):
        count = len(self.__datas_for_req_get)
        for i in range(count):
            # os.system('cls')
            print('正在下载招生院校信息:[{}/{}]'.format(i + 1, count))
            self.__data.extend(self.__req_data_on_page(data=self.__datas_for_req_get[i]))

        self.__store_in_db()

    def __req_data_on_page(self, data):

        result_list = []
        max_page = None
        while True:
            page_text = requests.post(url=self.url, data=data).text

            soup = BeautifulSoup(page_text, 'html.parser')

            if len(soup.select('table tbody tr')) == 1 and soup.select_one('table tbody .noResult'):
                break

            tr_list = soup.select(".ch-table tbody tr")
            for i in tr_list:
                url = 'https://yz.chsi.com.cn' + i.select_one('td form a').get('href')
                zsdw = (re.sub('\(.*?\)', '', i.select_one('td form a').text))
                local = (re.sub('\(.*?\)', '', i.select('td')[1].text))
                yjsy = i.select('td')[2].select('i').__len__()
                zzhxyx = i.select('td')[3].select('i').__len__()
                bsd = i.select('td')[4].select('i').__len__()

                lds = (zsdw, local, yjsy, zzhxyx, bsd, url)

                result_list.append(lds)

            max_page = yzw_table.get_max_page(soup) if max_page is None else max_page

            now_page = yzw_table.get_now_page(soup)
            print('共{}页，当前第{}页'.format(max_page, now_page))

            if now_page == max_page:
                break
            else:
                next_page = 1 + now_page
                data['pageno'] = next_page

        return result_list

    def __store_in_db(self):
        cur.executemany('INSERT INTO recruit_school (zsdw, local, yjsy, zzhxyx, bsd, url)'
                        ' VALUES (?,?,?,?,?,?)', self.__data)
        con.commit()


class yzw_table:

    @staticmethod
    def get_max_page(soup):
        '''
        此方法当前仅当页面处于第一页时有效
        :param soup:
        :return: 最大页码
        '''

        lip_list = soup.select('.ch-page .lip')
        for i in range(len(lip_list)):
            if 'dot' in lip_list[i].get('class'):
                k = i + 1
                break
        else:
            k = len(lip_list) - 2
        max_page_str = lip_list[k].select_one('a').text

        return int(max_page_str)

    @staticmethod
    def get_now_page(soup):

        now_page = soup.select_one('.lip.selected a').text
        return int(now_page)


@staticmethod
class dl_yzw:
    def __init__(self):
        self.dl_majors = dl_majors()
        self.dl_schools = dl_schools()
