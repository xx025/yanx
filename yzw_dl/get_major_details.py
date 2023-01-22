from bs4 import BeautifulSoup

from _g.g2 import GLOBAL_VAL
from _g.g3 import global_queue
from stools.sk2 import remove_spaces
from stools.sk3 import req_get


class dl_details:
    def __init__(self, ids):
        self.__data = []
        self.__urls = []

        self.__ids = ids
        self.task_id = str(GLOBAL_VAL['TASK_ID'])

    def dl_data(self):
        """
         return: zhao_sheng_zhuan_ye_d, kao_shi_fan_wei_d
        """

        if len(self.__urls) == 0:
            self.__set_urls()

        zhao_sheng_zhuan_ye_d = []
        kao_shi_fan_wei_d = []
        count = len(self.__urls)
        for l_j in range(len(self.__urls)):
            k = self.__urls[l_j]
            soup = BeautifulSoup(req_get(k).text, features="html.parser")

            zsdw = soup.select('.zsml-condition tbody tr .zsml-summary')
            zsdw = [remove_spaces(i.text) for i in zsdw]

            sid = k.split('=')[-1]
            enrollment_unit = zsdw[0]
            examination_method = zsdw[1]
            departments = zsdw[2].split(')')[-1]
            major = zsdw[3]
            learning_style = zsdw[4]
            research_direction = zsdw[5]
            instructor = zsdw[6]
            number_of_proposed_recruits = zsdw[7]

            data = (sid, self.task_id, enrollment_unit, examination_method, departments, major, learning_style,
                    research_direction, instructor, number_of_proposed_recruits)
            zhao_sheng_zhuan_ye_d.append(data)
            scope_items = soup.select('.zsml-result .zsml-res-items')
            data2 = []
            for i in scope_items:
                td = [sid, self.task_id]
                td2 = [remove_spaces(k.contents[0]) for k in i.select('tr td')]
                td.extend(td2)
                data2.append(td)

            kao_shi_fan_wei_d.extend(data2)

            strd = f"正在下载考试信息：{l_j + 1} / {count}"

            go = {'type': '考试', 'val': int(100 * (l_j + 1) / count), 'text': strd}
            global_queue.put(str(go))

        return zhao_sheng_zhuan_ye_d, kao_shi_fan_wei_d

    def __set_urls(self):

        self.__urls = ['https://yz.chsi.com.cn/zsml/kskm.jsp?id=' + i for i in self.__ids]
