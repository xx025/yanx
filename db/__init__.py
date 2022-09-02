import os
import sqlite3


class db_con:
    def __init__(self):
        self.T = None
        self.con = None
        self.cur = None

    def get_con(self):
        self.con = sqlite3.connect(os.getcwd() + '\db\database.db', check_same_thread=False)
        return self.con

    def get_cur(self):
        return self.con.cursor()


con_data = db_con()


def del_tables():
    cur.execute('DELETE  from 专业代码')
    cur.execute('DELETE  from 招生院校索引')
    cur.execute('DELETE  from 招生专业索引')
    cur.execute('DELETE  from 考试范围')
    cur.execute('DELETE  from 招生专业')


con = con_data.get_con()
cur = con_data.get_cur()
del_tables()

# cur.execute('DELETE  from xuekemenlei_code')
# cur.execute('DELETE  from xuekelingyu_code')
