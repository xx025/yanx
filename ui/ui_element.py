from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QLabel


def openurl(url):
    QDesktopServices.openUrl(QUrl(url))


class MyLabel(QLabel):

    def __int__(self):
        super(MyLabel, self).__init__()

    def setUrl(self, url):
        self.url = url

    def mousePressEvent(self, e):  # 单击
        openurl(self.url)
