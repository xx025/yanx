import requests
from bs4 import BeautifulSoup

from db import cur, con
from deal_text import replace_bank


class dl_details:
    def __init__(self):
        self.__data = []
        self.__urls = []

    def dl_data(self):
        if len(self.__urls) == 0:
            self.set_urls()

        count = len(self.__urls)
        for l_j in range(len(self.__urls)):
            k = self.__urls[l_j]
            soup = BeautifulSoup(requests.get(k).text, features="html.parser")

            zsdw = soup.select('.zsml-condition tbody tr .zsml-summary')
            zsdw = [replace_bank(i.text) for i in zsdw]

            sid = k.split('=')[-1]
            enrollment_unit = zsdw[0]
            examination_method = zsdw[1]
            departments = zsdw[2].split(')')[-1]
            major = zsdw[3]
            learning_style = zsdw[4]
            research_direction = zsdw[5]
            instructor = zsdw[6]
            number_of_proposed_recruits = zsdw[7]

            row1 = (sid, enrollment_unit, examination_method, departments, major, learning_style,
                    research_direction, instructor, number_of_proposed_recruits)

            cur.execute(
                'insert into recruit_details (id, enrollment_unit, examination_method, '
                'departments, major, learning_style, research_direction, instructor, number_recruit) '
                'VALUES (?,?,?,?,?,?,?,?,?)', row1
            )
            scope_items = soup.select('.zsml-result .zsml-res-items')
            data = []
            for i in scope_items:
                td = [replace_bank(k.text) for k in i.select('tr td')]
                td.insert(0, sid)
                data.append(td)
            cur.executemany(
                'INSERT INTO exam_scope (id, political, foreign_language, pro_course_1, pro_course_2) '
                'VALUES (?,?,?,?,?)', data)
            con.commit()

            print(row1)
            for j in data:
                print(j)
            print('{}/{}'.format(l_j, count))

    def set_urls(self):
        cons = cur.execute('select ksfw from recruit_major')
        self.__urls = ['https://yz.chsi.com.cn/zsml/kskm.jsp?id=' + i[0] for i in cons]
