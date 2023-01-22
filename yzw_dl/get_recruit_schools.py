from bs4 import BeautifulSoup

from _g import global_queue, GLOBAL_VAL
from db2 import get_abquy, get_uis11_list
from stools.sk2 import get_url_param
from stools.sk3 import req_post
from uns import list985, list211
from yzw_dl.yzw_pages import yzw_table


class dl_schools:
    def __init__(self):
        self.__url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
        self.__datas_for_req_get = []

        self.__data = []

    def dl_data(self):

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

        gcodes = GLOBAL_VAL['gcodes']
        params = {'ssdm': '',
                  'dwmc': '',
                  'mldm': gcodes['门类代码'],
                  'mlmc': '',
                  'yjxkdm': gcodes['学科代码'],
                  'zymc': gcodes['专业名称'],
                  'xxfs': gcodes['学习方式']
                  }

        rule_yxqu = GLOBAL_VAL['gcodes']['院校区域']
        '''
        rule_yxqu: 院校区域
        '''

        if not rule_yxqu:
            ssdms = ['']
        else:
            if rule_yxqu in ('a', 'b'):
                ssdms = get_abquy(rule_yxqu)
            else:
                ssdms = [rule_yxqu]

        len_of_all_ssdm, k = len(ssdms), 1
        for ssdm in ssdms:
            strd = f"正在下载院校信息{k}/{len_of_all_ssdm}"
            k += 1
            go = {'type': '学校', 'val': int(100 * (1) / 1), 'text': strd}
            global_queue.put(str(go))

            params['ssdm'] = ssdm
            tmp_data = self.__req_data_on_page(data=params)

            self.__data.extend(tmp_data)

        return self.__data

    def __req_data_on_page(self, data):

        result_list = []
        max_page = None
        while True:
            page_text = req_post(url=self.__url, data=data).text

            soup = BeautifulSoup(page_text, 'html.parser')

            if len(soup.select('table tbody tr')) == 1 and soup.select_one('table tbody .noResult'):
                break

            tr_list = soup.select(".ch-table tbody tr")
            for i in tr_list:
                url = 'https://yz.chsi.com.cn' + i.select_one('td form a').get('href')
                ud = get_url_param(url=url)

                def trn(strd):
                    return strd if strd else ''

                ssdm = trn(ud.get('ssdm'))
                dwmc = trn(ud.get('dwmc'))
                mldm = trn(ud.get('mldm'))
                mlmc = trn(ud.get('mlmc'))
                yjxkdm = trn(ud.get('yjxkdm'))
                xxfs = trn(ud.get('xxfs'))
                zymc = trn(ud.get('zymc'))

                # 博士点 = True if i.select('td')[-1].select_one('i') else False

                lds = (ssdm, dwmc, mldm, mlmc, yjxkdm, xxfs, zymc)

                result_list.append(lds)

            max_page = yzw_table.get_max_page(soup) if max_page is None else max_page

            now_page = yzw_table.get_now_page(soup)
            if max_page > 1:
                global_queue.put('共{}页，当前第{}页'.format(max_page, now_page))

            if now_page == max_page:
                break
            else:
                next_page = 1 + now_page
                data['pageno'] = next_page

        return result_list


def get_dwmc(rules=None, ls=None):
    """
    根据院校建设计划条件筛选对应的院校
    在下载院校阶段对院校进行筛选，
    """
    ls2 = []

    rule = rules[0]

    if not rule:
        return ls
    else:
        if rule in ('985', '211', '11'):
            if rule == '985':
                # 985院校
                u_list = list985
            elif rule == '211':
                u_list = list211
                # 211院校
            else:
                # 双一流院校
                u_list = get_uis11_list()
            for k in ls:
                if k[1] in u_list:
                    ls2.append(k)
        else:
            zdyx = set(list985) | set(list211) | set(get_uis11_list())
            # 普通院校
            for k in ls:
                if k[1] not in zdyx:
                    ls2.append(k)
    return ls2
