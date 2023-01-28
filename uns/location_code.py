# import json
#
# from db2 import db_con
# from stools.sk3 import req_get
# from uns import loc_A, loc_B
#
#
# class location_code:
#     def __init__(self):
#         self.__url = 'https://yz.chsi.com.cn/zsml/pages/getSs.jsp'
#         self.__data = []
#
#     def __req_data(self):
#         json_data = json.loads(req_get(self.__url).text)
#
#         def check(str1):
#             for i in loc_A:
#                 if i in str1:
#                     return 'a'
#             for i in loc_B:
#                 if i in str1:
#                     return 'b'
#
#         for k in json_data:
#             self.__data.append((k['dm'], k['mc'], check(k['mc'])))
#
#         self.__store_in_db()
#
#     def get_data(self, ab: str):
#         con = db_con.get_con()
#         cur = con.cursor()
#         if ab in ('a', 'b'):
#             cursor = cur.execute("SELECT *  FROM 地区代码 where ab=?", (ab,))
#         else:
#             cursor = cur.execute("SELECT *  FROM 地区代码 ")
#
#         data = [(i[0], i[1], i[2]) for i in cursor]
#
#         con.commit()
#         con.close()
#         if len(data) == 0:
#             self.__req_data()
#             return self.get_data(ab=ab)
#         else:
#             return data
#
#     def __store_in_db(self):
#         """
#          数据库表设计
#              地区代码 地区名称 AB区
#          :return:None
#          """
#         try:
#
#             con = db_con.get_con()
#             cur = con.cursor()
#             cur.executemany('INSERT INTO 地区代码 (dm, mc,ab) VALUES (?,?,?)', self.__data)
#             con.commit()
#             con.close()
#         except Exception:
#             print(Exception)
