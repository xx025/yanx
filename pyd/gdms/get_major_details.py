from bs4 import BeautifulSoup

from pyd import rsp
from pyd.pys.global_values import global_queue
from pyd.re_spaces import remove_spaces


class dl_details:
    def __init__(self, con):
        self.__data = []
        self.__urls = []
        self.__con = con
        self.__cur = self.__con.cursor()

    def dl_data(self):
        if len(self.__urls) == 0:
            self.__set_urls()

        count = len(self.__urls)
        for l_j in range(len(self.__urls)):
            k = self.__urls[l_j]
            soup = BeautifulSoup(rsp.get(k).text, features="html.parser")

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

            data = (sid, enrollment_unit, examination_method, departments, major, learning_style,
                    research_direction, instructor, number_of_proposed_recruits)
            self.__store_in_database_major(data=data)
            scope_items = soup.select('.zsml-result .zsml-res-items')
            data2 = []
            for i in scope_items:
                td = [remove_spaces(k.contents[0]) for k in i.select('tr td')]
                td.insert(0, sid)
                data2.append(td)

            self.__store_in_database_scop(data=data2)

            global_queue.put('正在下载招生专业详情[{}/{}]'.format(l_j + 1, count))

    def __set_urls(self):

        cons = self.__cur.execute('select ID from 招生专业索引')
        self.__urls = ['https://yz.chsi.com.cn/zsml/kskm.jsp?id=' + i[0] for i in cons]

    def __store_in_database_major(self, data):
        try:
            self.__cur.execute(
                'insert into 招生专业 (id, enrollment_unit, examination_method, '
                'departments, major, learning_style, research_direction, instructor, number_recruit) '
                'VALUES (?,?,?,?,?,?,?,?,?)', data)
            self.__con.commit()
        except Exception:
            print(Exception)

    def __store_in_database_scop(self, data):
        try:
            self.__cur.executemany(
                'INSERT INTO 考试范围 (id, political, foreign_language, pro_course_1, pro_course_2) '
                'VALUES (?,?,?,?,?)', data)
            self.__con.commit()
        except Exception:
            print(Exception)
