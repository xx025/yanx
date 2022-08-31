import re
from copy import copy

import requests
from bs4 import BeautifulSoup

from dl_s.yzw_pages import yzw_table


class dl_schools:
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

    def dl_data(self, con, cur):
        count = len(self.__datas_for_req_get)
        for i in range(count):
            # os.system('cls')

            print(f'正在下载招生院校信息:[{i + 1}/{count}]')
            tmp_data = self.__req_data_on_page(data=self.__datas_for_req_get[i])
            print(' '.join([kl[:2][0] for kl in tmp_data]))

            self.__data.extend(tmp_data)

        self.__store_in_db(con, cur)

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
            if max_page > 1:
                print('共{}页，当前第{}页'.format(max_page, now_page))

            if now_page == max_page:
                break
            else:
                next_page = 1 + now_page
                data['pageno'] = next_page

        return result_list

    def __store_in_db(self, con, cur):

        cur.executemany('INSERT INTO recruit_school (zsdw, local, yjsy, zzhxyx, bsd, url)'
                        ' VALUES (?,?,?,?,?,?)', self.__data)
        con.commit()
