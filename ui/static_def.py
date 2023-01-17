# 创建任务的名称和ID
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox

from _g import global_queue
from ui.ui_texts import GITHUBPAGE3, version_id, UPDATE, version_build


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


def out_date():
    upd = UPDATE
    local = upd.get('local')
    if local:
        # 本地数据
        import datetime
        curr_date = version_id
        curr_date_temp = datetime.datetime.strptime(curr_date, "%Y%m%d")
        new_date = curr_date_temp + datetime.timedelta(days=30)
        now = datetime.datetime.now()
        show = now > new_date

        if show:
            mesg = upd.get('update_mes')
            reply = QMessageBox.question(QtWidgets.QMainWindow(),
                                         "Hello",
                                         mesg,
                                         QMessageBox.No | QMessageBox.Yes)

            if reply == 16384:
                opurl(GITHUBPAGE3)
            else:
                sys.exit()

    else:

        # 云端数据
        if version_id in upd.get("retention"):
            show = False
        else:
            show = version_id != upd["latest_version"].get('id')

        if show:
            mesg = f"当前版本{version_build},最新版本{upd.get('latest_version').get('v')}," + upd.get('update_mes')
            reply = QMessageBox.question(QtWidgets.QMainWindow(),
                                         "Hello",
                                         mesg,
                                         QMessageBox.No | QMessageBox.Yes)
            if reply == 16384:
                opurl(GITHUBPAGE3)
            sys.exit()


def opurl(url):
    QDesktopServices.openUrl(QUrl(url))
