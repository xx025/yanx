from bs4 import BeautifulSoup

import stools
import stools.sk2
from _g.g3 import global_queue

from stools.sk3 import req_get
from yzw_dl.yzw_pages import yzw_table


class dl_majors:
    def __init__(self, xue_xiao_lie_biao):
        self.__rules = None
        self.__urls = []
        self.__xue_xiao_lie_biao = xue_xiao_lie_biao
        self.__data = []

    def set_urls(self):

        for ks in self.__xue_xiao_lie_biao:
            u = 'https://yz.chsi.com.cn/zsml/querySchAction.do?' \
                'ssdm={}&dwmc={}&mldm={}&mlmc={}&yjxkdm={}&xxfs={}&zymc={}'. \
                format(ks[0], ks[1], ks[2], ks[3], ks[4], ks[5], ks[6])
            self.__urls.append(u)

    def dl_data(self):

        count: int = len(self.__urls)
        for i in range(count):
            tmp_data = self.__req_data_on_page(url=self.__urls[i])
            self.__data.extend(tmp_data)
            sd = f"正在下载专业信息{i + 1}/{count}"

            go = {'type': '专业', 'val': int(100 * (i + 1) / count), 'text': sd}
            global_queue.put(str(go))
        return self.__data

    def __req_data_on_page(self, url):
        next_page_url = url + '&pageno='
        result_list = []
        max_page = None
        while True:
            page_text = req_get(url=url).text
            soup = BeautifulSoup(page_text, 'html.parser')
            for k in soup.select('.zsml-list-box tbody tr'):
                ksfw = stools.sk2.get_url_param(k.select('td')[7].select_one('a').get('href')).get('id')
                # 只获取一个id
                #     def __set_urls(self):
                #
                #         cons = self.__cur.execute('select ID from 招生专业索引')
                #         self.__urls = ['https://yz.chsi.com.cn/zsml/kskm.jsp?id=' + i[0] for i in cons]
                result_list.append(ksfw)

            max_page = yzw_table.get_max_page(soup) if max_page is None else max_page

            now_page = yzw_table.get_now_page(soup)
            if max_page > 1:
                global_queue.put('共{}页，当前第{}页'.format(max_page, now_page))
            if now_page == max_page:
                break
            else:
                next_page = 1 + now_page
                url = next_page_url + str(next_page)
        return result_list
