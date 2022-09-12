import csv
import datetime
import winreg

from pyd.db import db_con
from pyd.pys.global_values import GLOBALS_DICT, global_queue


# https://www.jb51.net/article/181007.htm
# CSV文件输出乱码问题
# Sqlite 字符串截取 substr https://www.techonthenet.com/sqlite/functions/substr.php
def out_csv():
    now = datetime.datetime.now()
    try:
        path = desktop_path() + r'\{}-{}-{}.csv'.format(GLOBALS_DICT['file_name'], now.date(), now.second)
        path = path.replace(' ', '')
        with open(path, 'a', encoding='utf-8-sig', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ['学校', '所在地', 'AB区', '985院校', '211院校', '双一流院校', '考试方式', '学院', '专业', '学习方式',
                 '招生人数', '政治考试', '外语考试',
                 '专业课1考试', '专业课二考试'])

            con = db_con.get_con()

            data = [i for i in con.execute('''select 招生专业.id,
       院校库.院校名称,
       院校库.所在地,
       院校库.AB,
       院校库.IS985,
       院校库.IS211,
       院校库.双一流,
       招生专业.examination_method,
       招生专业.departments,
       招生专业.major,
       招生专业.learning_style,
       招生专业.number_recruit
FROM 招生专业,
     院校库
where substr(招生专业.id, 0, 6) == 院校库.院校代码''')]
            for i in data:
                d1 = list(i)[1:]
                data2 = []
                for k in [i for i in con.execute('select * from 考试范围 where id=?', (i[0],))]:
                    u2 = [u for u in k][1:]
                    data2.extend(u2)
                d1.extend(data2)
                writer.writerow(d1)
            con.close()
        GLOBALS_DICT['out_path'] = path

        global_queue.put('导出完成')
        global_queue.put('导出目录' + GLOBALS_DICT['out_path'])

    except Exception:
        print(Exception)


def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path
