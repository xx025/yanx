import json
import os

import requests

from db import cur, con
from edus import loc_A, loc_B


def show_codes(data: list):
    r_dict = dict()
    for i in range(data.__len__()):
        r_dict[data[i][0]] = data[i][1]
        if i != 0 and i % 5 == 0:
            print('\n', end='')
        print(' ' * 3 + data[i][1] + ':' + data[i][0] + '\t', end='')
    else:
        print('\n', end='')

    return r_dict


# class choice:
#     def __init__(self):
#
#         self.__construction_plans = {'211': '0', '985': '0', '11': '0'}
#         self.__learn_mode = None
#         self.majors = None
#         self.__location_codes = None
#         self.xkml_code = None
#
#     def location(self):
#         """
#         5.选择地区
#         :return:
#         """
#         print('''
# 5. 选择地区
#     此项为非必选，如果你不做选择按回车键即可
#
#     选择地区，是排除性选择，选择某些地区就会排除掉未选择的地区，但同时你选择的
#     地区未必有你选择的招生院校或专业
#             ''')
#
#         ab = input('是否选择区分A区或B区?(A区：a ,B区：b ，不做区分按回车键 ):')
#
#         data = location_code()
#         locs = data.get_data(ab)
#
#         sel_d = show_codes(locs)
#
#         print('''
# 请根据上面的地区选择地区， 输入省市后面的代码（如北京市：11）,
# 选择多个请用空格隔开,选择全部敲回车键 :
#
#         ''')
#
#         input_str = input('''请选择：''').strip()
#
#         if ab != 'a' and ab != 'b' and input_str == '':
#             # 对所有地区不做选择
#             self.__location_codes = None
#         else:
#             self.__location_codes = []
#             if input_str == '':
#                 self.__location_codes = [i[0] for i in locs]
#             else:
#                 tmp_locations = input_str.split(' ')
#                 for i in tmp_locations:
#                     if i in sel_d:
#                         self.__location_codes.append(i)
#
#             print('你的选择：')
#             k = 0
#             for i in self.__location_codes:
#                 print(' ' * 3 + i + ':' + sel_d[i], end='')
#                 k += 1
#                 if k % 5 == 0:
#                     print()
#             else:
#                 print()
#
#         input('\n回车继续')
#         os.system('cls')
#
#         return self.__location_codes
#
#     def discipline(self):
#
#         self.xkml_code = xkml_code()
#         os.system('cls')
#         print('''
# 1. 选择门类(*必选)
#     选择学硕或专硕，
#     1. 如果选择学硕请输入学硕门类后的代码(只能选择一个)
#     2. 如果你选择专硕，请输入:zyxw
#                     ''')
#         print('学术学位（学硕）：')
#         d = show_codes(self.xkml_code.get_data())
#         print('专业学位（专硕）：')
#         print(' ' * 3 + '专业学位：zyxw')
#         re = input('\n请选择:')
#         while True:
#             if re in d:
#                 print('你的选择：学术学位' + re + d[re])
#                 break
#             elif re == 'zyxw':
#                 print('你的选择：zyxw 专业学位')
#                 break
#             else:
#                 print('选择错误')
#                 re = input('重新选择：')
#         return re
#
#     def major(self, ly_code):
#         print('''
# 3. 选择专业
#     此项为非必选，如果你不做选择按回车键即可
#                     ''')
#         zy = zy_name(ly_code=ly_code)
#         zy_data = zy.get_data()
#         the_in = input('你选择的领域共有' + str(len(zy_data)) + '个专业，是否选择具体专业？（是输入:y,否输入:n）:')
#
#         if the_in == 'y':
#             self.majors = []
#             zy = show_codes(zy_data)
#             input_str = input('\n请输入专业后面的代码，选择多个请用空格隔开：').strip()
#
#             tmp_list = input_str.split(' ')
#             for code in tmp_list:
#                 if code in zy:
#                     self.majors.append(zy[code])
#             else:
#                 print('\n你的选择：')
#                 for i in range(self.majors.__len__()):
#                     print(self.majors[i], end='\t')
#                     if (i != 0 and i % 5 == 0) or (i + 1) == self.majors.__len__():
#                         print()
#
#         input('\n回车继续')
#         os.system('cls')
#
#         return self.majors
#
#     def construction_plan(self):
#         print('''
# 6. 选择院校建设计划
#     你是否选择学校是否是 双一流（111） 、985 或 211 院校，
#     如果选择选择请输入111、985 或 211 如果选择多项请加空格并依次输入
#     如果不做选择，请输入回车
#                     ''')
#
#         tmp_list = input('请选择：').strip().split(' ')
#
#         if tmp_list == ['']:
#             pass
#         else:
#             for code in tmp_list:
#                 if code in ['211', '985', '11']:
#                     self.__construction_plans[code] = '1'
#             print('你的选择：')
#             for i in self.__construction_plans.items():
#                 print(' ' * 3 + str(i), end='\t')
#             print()
#
#         input('\n回车继续')
#         os.system('cls')
#
#         return self.__construction_plans
#
#     def field_of_study(self, dm):
#         """
#         2. 选择领域
#         :return:
#         """
#         os.system('cls')
#         print('''
# 2.选择领域(*必选)
#     请根据选择面的学科领域选择一个领域，并输入领域后的代码(只能选择一个)
#                     ''')
#         m = xkly_code(dm=dm)
#         d = show_codes(m.get_data())
#         input_str = input('\n请选择：')
#         while True:
#             if input_str in d:
#                 print('你的选择：' + input_str + d[input_str])
#                 break
#             else:
#                 print('选择错误')
#                 input_str = input('重新选择:')
#
#         input('\n回车继续')
#         os.system('cls')
#
#         return input_str
#
#     def learn_code(self):
#         """
#         4. 选择学习方式
#         :return:
#         """
#         print('''
# 4. 选择学习方式
#     全日制：1 ,非全日制：2 ,不做选择回车即可 ''')
#         xxfs = input('请选择：')
#         self.__learn_mode = xxfs if xxfs in ['1', '2'] else None
#
#         input('\n回车继续')
#         os.system('cls')
#
#         return self.__learn_mode


class location_code:
    def __init__(self):
        self.__url = 'https://yz.chsi.com.cn/zsml/pages/getSs.jsp'
        self.__data = []

    def __req_data(self):
        json_data = json.loads(requests.get(self.__url).text)

        def check(str1):
            for i in loc_A:
                if i in str1:
                    return 'a'
            for i in loc_B:
                if i in str1:
                    return 'b'

        for k in json_data:
            self.__data.append((k['dm'], k['mc'], check(k['mc'])))

        self.__store_in_db()

    def get_data(self, ab: str):
        if ab in ('a', 'b'):
            cursor = cur.execute("SELECT *  FROM location_code where ab=?", (ab,))
        else:
            cursor = cur.execute("SELECT *  FROM location_code ")

        data = [(i[0], i[1], i[2]) for i in cursor]
        if len(data) == 0:
            self.__req_data()
            return self.get_data(ab=ab)
        else:
            return data

    def __store_in_db(self):
        """
        数据库表设计
            地区代码 地区名称 AB区
        :return:None
        """
        cur.execute('DELETE FROM location_code')
        cur.executemany('INSERT INTO location_code (dm, mc,ab) VALUES (?,?,?)', self.__data)
        con.commit()


class xkml_code:

    def __init__(self):
        self.url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'
        self.__data = []

    def __req_data(self):
        json_data = json.loads(requests.get(self.url).text)
        self.__data = [(k['dm'], k['mc']) for k in json_data]
        self.__store_in_db()

    def __store_in_db(self):
        """
        数据库表设计
            学位代码 学位名称
        :return:None
        """
        cur.execute('DELETE FROM xuekemenlei_code')
        cur.executemany('INSERT INTO xuekemenlei_code (dm, mc) VALUES (?,?)', self.__data)
        con.commit()

    def get_data(self):
        cursor = cur.execute("SELECT *  FROM xuekemenlei_code")

        data = [(i[0], i[1]) for i in cursor]
        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data


class xkly_code:
    def __init__(self, dm):
        self.url = 'https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
        self.__data = []
        self.__mldm = dm

    def __req_data(self):
        # 获取学科门类或领域
        r = requests.post(url=self.url, data={'mldm': self.__mldm}).text
        self.__data = [(self.__mldm, k['mc'], k['dm']) for k in json.loads(r)]
        self.__store_in_db()

    def __store_in_db(self):
        cur.executemany('INSERT INTO xuekelingyu_code (xkml, mc, dm)values (?,?,?)', self.__data)
        con.commit()

    def get_data(self):
        cursor = cur.execute("SELECT *  FROM xuekelingyu_code where xkml=?", (self.__mldm,))
        data = [(i[2], i[1]) for i in cursor]

        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data


class zy_name:
    def __init__(self, ly_code):
        self.url = 'https://yz.chsi.com.cn/zsml/code/zy.do'
        self.data = []
        self.__ly_code = ly_code

    def __req_data(self):

        r = requests.post(url=self.url, data={'q': self.__ly_code}).text
        req_data = json.loads(r)
        self.__data = [(self.__ly_code, req_data[i], str(i + 1)) for i in range(len(req_data))]
        self.__store_in_db()

    def __store_in_db(self):
        cur.execute('DELETE FROM zhuanye_name')
        cur.executemany('INSERT INTO zhuanye_name (zy_code, name,dm) VALUES (?,?,?)', self.__data)
        con.commit()

    def get_data(self):
        cursor = cur.execute("SELECT dm,name  FROM zhuanye_name where zy_code=?", (self.__ly_code,))
        data = [i for i in cursor]
        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data
