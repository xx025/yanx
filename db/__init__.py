import os
import sqlite3


class db_con:
    def __init__(self):
        self.con = None
        self.cur = None

    def get_con(self):
        self.con = sqlite3.connect(os.getcwd() + '\db\database.db', check_same_thread=False)
        return self.con

    def get_cur(self):
        return self.con.cursor()


con_data = db_con()
con = con_data.get_con()
cur = con_data.get_cur()

# cur.execute('DELETE  from xuekemenlei_code')
# cur.execute('DELETE  from xuekelingyu_code')
cur.execute('DELETE  from zhuanye_name')
cur.execute('DELETE  from recruit_school')
cur.execute('DELETE  from recruit_major')
cur.execute('DELETE  from recruit_details')
cur.execute('DELETE  from exam_scope')
