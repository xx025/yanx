import sqlite3





con = sqlite3.connect('../database.db')
print("数据库打开成功")
cur=con.cursor()