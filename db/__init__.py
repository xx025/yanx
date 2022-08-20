import os
import sqlite3

con = sqlite3.connect(os.getcwd() + '\db\database.db')
cur = con.cursor()

cur.execute('DELETE  from xuekemenlei_code')
cur.execute('DELETE  from xuekelingyu_code')
cur.execute('DELETE  from zhuanye_name')
cur.execute('DELETE  from recruit_school')
cur.execute('DELETE  from recruit_major')
