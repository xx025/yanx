import os
import sqlite3

from global_values import global_queue


class db_con:

    @staticmethod
    def get_con():
        con = sqlite3.connect(os.getcwd() + '\db\database.db', check_same_thread=False)
        return con


def kks():
    global_queue.put('正在初始化数据库')
    con = db_con.get_con()
    cur = con.cursor()
    cur.execute('DELETE  from 招生院校索引')
    cur.execute('DELETE  from 招生专业索引')
    cur.execute('DELETE  from 考试范围')
    cur.execute('DELETE  from 招生专业')
    con.commit()
    con.close()
    global_queue.put('初始化数据库完成')
