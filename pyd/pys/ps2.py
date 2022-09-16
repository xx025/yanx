import time

import requests
from PyQt5.QtCore import pyqtSignal, QThread

from pyd.pys.global_values import global_queue
from pyd.user import user


class UpdateThread(QThread):
    # 创建一个信号，触发时传递当前时间给槽函数
    update_data = pyqtSignal(str)

    def run(self):
        while True:
            if not global_queue.empty():
                for i in range(global_queue.qsize()):
                    self.update_data.emit(global_queue.get())
                    time.sleep(0.1)
            time.sleep(0.1)


def t1x(data3):
    user1 = user()
    user1.set_location(loca_code=data3.get('地区'))
    user1.set_discipline(code=data3.get('门类'))

    user1.set_field_of_study(code=data3.get('领域'))

    user1.set_construction_plans(code=data3.get('建设计划'))
    user1.set_learn_way(code=data3.get('学习方式'))

    user1.dl_all()
    global_queue.put('下载完成')


def get_Latest_Announcements():
    textssss = '''或许由于github连接原因，你没有获取到最新公告，关注：https://yanx.loefairy.top/ 获取最新动态'''
    try:
        url = 'https://gist.githubusercontent.com/xx025/904e719c8a74be36176ef167df82fc3b/raw/'
        textssss = '公告：\n' + requests.get(url, timeout=4).text
    except Exception:
        pass
    return textssss
