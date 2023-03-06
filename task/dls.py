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

from _g.g2 import GLOBAL_VAL
from _g.g3 import global_queue
from db2 import daochu_xinxi
from utils.get_path import get_desktop_path


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
            with open(path, 'w', encoding='utf-8-sig', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data4)

            global_queue.put('导出完成')

    t1 = threading.Thread(target=f1, args=tuple())
    t1.setDaemon(True)
    t1.start()


