import requests
from bs4 import BeautifulSoup

from processing_string import replace_bank
from processing_string.print_string import print_t


class dl_details:
    def __init__(self):
        self.__data = []
        self.__urls = []

    def dl_data(self, con, cur):
        if len(self.__urls) == 0:
            self.set_urls(con, cur)

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

            data = (sid, enrollment_unit, examination_method, departments, major, learning_style,
                    research_direction, instructor, number_of_proposed_recruits)

            scope_items = soup.select('.zsml-result .zsml-res-items')
            data2 = []
            for i in scope_items:
                td = [replace_bank(k.contents[0]) for k in i.select('tr td')]
                td.insert(0, sid)
                data2.append(td)

            self.store_in_database_scop(data=data, con=con, cur=cur)
            self.store_in_database_scop(data=data2, con=con, cur=cur)

            print_t('正在下载招生专业详情[{}/{}]'.format(l_j, count))

    def set_urls(self, con, cur):
        cons = cur.execute('select ID from 招生专业索引')
        self.__urls = ['https://yz.chsi.com.cn/zsml/kskm.jsp?id=' + i[0] for i in cons]

    @staticmethod
    def store_in_database_major(data, con, cur):
        try:
            cur.execute(
                'insert into 招生专业 (id, enrollment_unit, examination_method, '
                'departments, major, learning_style, research_direction, instructor, number_recruit) '
                'VALUES (?,?,?,?,?,?,?,?,?)', data
            )
            con.commit()
        except Exception:
            print(Exception)

    @staticmethod
    def store_in_database_scop(data, con, cur):
        try:
            cur.executemany(
                'INSERT INTO 考试范围 (id, political, foreign_language, pro_course_1, pro_course_2) '
                'VALUES (?,?,?,?,?)', data)
            con.commit()
        except Exception:
            print(Exception)
