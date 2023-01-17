# https://www.jb51.net/article/181007.htm
# CSV文件输出乱码问题
# Sqlite 字符串截取 substr https://www.techonthenet.com/sqlite/functions/substr.php

'''

导出文件模块

'''
import csv
import datetime
import os
import threading

from _g import GLOBAL_VAL, global_queue
from db2 import db_con, daochu_xinxi
from stools.sk2 import get_desktop_path


def dao_chu_ren_wu():
    global_queue.put('开始导出')

    def f1():
        selected_ids = GLOBAL_VAL['TASK_SELECTED']['ids']
        selected_texts = GLOBAL_VAL['TASK_SELECTED']['texts']

        print(selected_ids)
        print(selected_texts)

        if len(selected_ids) > 0:
            if len(selected_ids) == 1:
                # 导出单个任务
                filename = selected_texts[0]
            else:
                # 导出多个任务
                filename = '合并' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            path = os.path.join(get_desktop_path(), f'{filename}.csv')

            data4 = daochu_xinxi(selected_ids)
            with open(path, 'a', encoding='utf-8-sig', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data4)

            global_queue.put('导出完成')

    t1 = threading.Thread(target=f1, args=tuple())
    t1.setDaemon(True)
    t1.start()


def shan_chu_ren_wu():
    # (伪)删除，available 变成0
    con = db_con.get_con()
    cur = con.cursor()
    selected_ids = GLOBAL_VAL['TASK_SELECTED']['ids']

    sqlm = [(id,) for id in selected_ids]
    cur.executemany('update 下载任务 set available=0 where id=?', sqlm)
    con.commit()
    con.close()