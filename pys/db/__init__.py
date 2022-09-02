import os
import sqlite3


class db_con:

    @staticmethod
    def get_con():
        con = sqlite3.connect(os.getcwd() + '\db\database.db', check_same_thread=False)
        return con


def kks():
    con = db_con.get_con()
    cur = con.cursor()
    cur.execute('DELETE  from 专业代码')
    cur.execute('DELETE  from 招生院校索引')
    cur.execute('DELETE  from 招生专业索引')
    cur.execute('DELETE  from 考试范围')
    cur.execute('DELETE  from 招生专业')
    con.commit()
    con.close()


kks()

