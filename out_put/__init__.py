import csv
import datetime
import os

from db import con
from global_values import GLOBALS_DICT


# https://www.jb51.net/article/181007.htm
# CSV文件输出乱码问题

def out_csv():
    now = datetime.datetime.now()
    try:
        path = os.getcwd() + r'\{}-{}-{}.csv'.format(GLOBALS_DICT['file_name'], now.date(), now.second)
        path = path.replace(' ', '')
        with open(path, 'a', encoding='utf-8-sig', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ['学校', '考试方式', '学院', '专业', '学习方式', '研究方向', '导师', '招生人数', '政治考试', '外语考试',
                 '专业课1考试', '专业课二考试'])
            data = [i for i in con.execute('select * from recruit_details ')]
            for i in data:
                d1 = list(i)[1:]
                data2 = []
                for k in [i for i in con.execute('select * from exam_scope where id=?', (i[0],))]:
                    u2 = [u for u in k][1:]
                    data2.extend(u2)
                d1.extend(data2)
                writer.writerow(d1)
        GLOBALS_DICT['out_path'] = path

    except Exception as e:
        print(Exception)
