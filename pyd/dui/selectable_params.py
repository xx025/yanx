import json

from pyd import rsp
from pyd.db import db_con

from pyd.gul import loc_A, loc_B


class location_code:
    def __init__(self):
        self.__url = 'https://yz.chsi.com.cn/zsml/pages/getSs.jsp'
        self.__data = []

    def __req_data(self):
        json_data = json.loads(rsp.get(self.__url).text)

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
        con = db_con.get_con()
        cur = con.cursor()
        if ab in ('a', 'b'):
            cursor = cur.execute("SELECT *  FROM 地区代码 where ab=?", (ab,))
        else:
            cursor = cur.execute("SELECT *  FROM 地区代码 ")

        data = [(i[0], i[1], i[2]) for i in cursor]

        con.commit()
        con.close()
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
        try:

            con = db_con.get_con()
            cur = con.cursor()
            cur.executemany('INSERT INTO 地区代码 (dm, mc,ab) VALUES (?,?,?)', self.__data)
            con.commit()
            con.close()
        except Exception:
            print(Exception)


class xkml_code:

    def __init__(self):
        self.url = 'https://yz.chsi.com.cn/zsml/pages/getMl.jsp'
        self.__data = []

    def __req_data(self):
        json_data = json.loads(rsp.get(self.url).text)
        self.__data = [(k['dm'], k['mc']) for k in json_data]
        self.__store_in_db()

    def __store_in_db(self):
        """
        数据库表设计
            学位代码 学位名称
        :return:None
        """
        try:
            con = db_con.get_con()
            cur = con.cursor()
            cur.executemany('INSERT INTO 学科门类 (dm, mc) VALUES (?,?)', self.__data)
            con.commit()
            con.close()
        except Exception:
            print(Exception)

    def get_data(self):
        con = db_con.get_con()
        cur = con.cursor()
        cursor = cur.execute("SELECT *  FROM 学科门类")

        data = [(i[0], i[1]) for i in cursor]
        con.close()
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
        r = rsp.post(url=self.url, data={'mldm': self.__mldm}).text
        self.__data = [(self.__mldm, k['mc'], k['dm']) for k in json.loads(r)]
        self.__store_in_db()

    def __store_in_db(self):
        try:
            con = db_con.get_con()
            cur = con.cursor()
            cur.executemany('INSERT INTO 学科领域代码 (xkml, mc, dm)values (?,?,?)', self.__data)
            con.commit()
            con.close()
        except Exception:
            print(Exception)

    def get_data(self):
        try:
            con = db_con.get_con()
            cur = con.cursor()
            cursor = cur.execute("SELECT *  FROM 学科领域代码 where xkml=?", (self.__mldm,))
            data = [(i[2], i[1]) for i in cursor]
            con.close()
            if len(data) == 0:
                self.__req_data()
                return self.get_data()
            else:
                return data
        except Exception:
            print(Exception)


class zy_name:
    def __init__(self, ly_code):
        self.url = 'https://yz.chsi.com.cn/zsml/code/zy.do'
        self.data = []
        self.__ly_code = ly_code

    def __req_data(self):
        r = rsp.post(url=self.url, data={'q': self.__ly_code}).text
        req_data = json.loads(r)
        self.__data = [(self.__ly_code, req_data[i], str(i + 1)) for i in range(len(req_data))]
        self.__store_in_db()

    def __store_in_db(self):
        try:
            con = db_con.get_con()
            cur = con.cursor()
            cur.execute('DELETE FROM 专业代码')
            cur.executemany('INSERT INTO 专业代码 (zy_code, name,dm) VALUES (?,?,?)', self.__data)
            con.commit()
            con.close()
        except Exception:
            print(Exception)

    def get_data(self):
        con = db_con.get_con()
        cur = con.cursor()
        cursor = cur.execute("SELECT dm,name  FROM 专业代码 where zy_code=?", (self.__ly_code,))
        data = [i for i in cursor]
        con.close()
        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data
