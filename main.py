import os
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from addx import UpdateThread, t1x
from global_values import GLOBALS_DICT
from pys.db import kks
from pys.download_university_info.selectable_params import xkml_code, xkly_code
from pys.export_to_file import out_csv
from pys.user.main_win_choice import choice


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(843, 718)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setWindowIcon(QIcon(os.getcwd() + '/img/ico.ico'))
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(190, 50, 431, 71))
        self.textBrowser.setStyleSheet("border:0px")
        self.textBrowser.setObjectName("textBrowser")

        self.textBrowser1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser1.setGeometry(QtCore.QRect(40, 550, 741, 151))
        self.textBrowser1.setObjectName("textBrowser")

        self.textBrowser2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser2.setGeometry(QtCore.QRect(630, 20, 201, 71))
        self.textBrowser2.setObjectName("textBrowser")
        self.textBrowser2.setOpenExternalLinks(True)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 150, 811, 391))
        self.widget.setObjectName("widget")

        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(330, 320, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.dl_click)

        self.pushButton2 = QtWidgets.QPushButton(self.widget)
        self.pushButton2.setGeometry(QtCore.QRect(660, 320, 93, 28))
        self.pushButton2.setObjectName("pushButton2")

        self.pushButton2.clicked.connect(self.o_c_click)

        self.pushButton2.setVisible(False)

        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 771, 131))
        self.groupBox.setObjectName("groupBox")
        self.menleileibie_lable = QtWidgets.QLabel(self.groupBox)
        self.menleileibie_lable.setGeometry(QtCore.QRect(70, 30, 72, 15))
        self.menleileibie_lable.setObjectName("menleileibie_lable")
        self.xuanzexueke = QtWidgets.QComboBox(self.groupBox)
        self.xuanzexueke.setGeometry(QtCore.QRect(220, 70, 211, 41))
        self.xuanzexueke.setObjectName("xuanzexueke")
        self.xuanzexueke.addItem("")
        self.xuanzexueke.setEnabled(False)

        self.xuekeleibie_lable = QtWidgets.QLabel(self.groupBox)
        self.xuekeleibie_lable.setGeometry(QtCore.QRect(60, 80, 141, 21))
        self.xuekeleibie_lable.setObjectName("xuekeleibie_lable")
        self.xuanze_menlei = QtWidgets.QComboBox(self.groupBox)
        self.xuanze_menlei.setGeometry(QtCore.QRect(150, 20, 131, 31))
        self.xuanze_menlei.setEditable(False)
        self.xuanze_menlei.setObjectName("xuanze_menlei")
        self.xuanze_menlei.addItems(['选择门类', '专业学位', '学术学位'])
        self.xuanze_menlei.currentIndexChanged.connect(self.indexChange_xuan_ze_men_lei_1)

        self.xuanze_menlei_2 = QtWidgets.QComboBox(self.groupBox)
        self.xuanze_menlei_2.setGeometry(QtCore.QRect(300, 20, 121, 31))
        self.xuanze_menlei_2.setEditable(False)
        self.xuanze_menlei_2.setObjectName("xuanze_menlei_2")

        self.xuanze_menlei_2.setEnabled(False)
        self.xuanze_menlei_2.setVisible(False)

        self.xuanze_menlei_2.currentIndexChanged.connect(self.indexChange_xuan_ze_men_lei_2)

        self.xuanze_menlei_2.addItem("")
        self.xuanze_menlei_2.addItem("")

        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 170, 771, 121))
        self.groupBox_2.setObjectName("groupBox_2")

        self.edu_local_lable = QtWidgets.QLabel(self.groupBox_2)
        self.edu_local_lable.setGeometry(QtCore.QRect(340, 80, 72, 15))
        self.edu_local_lable.setObjectName("edu_local_lable")
        self.learn_mode_lable = QtWidgets.QLabel(self.groupBox_2)
        self.learn_mode_lable.setGeometry(QtCore.QRect(80, 30, 72, 15))
        self.learn_mode_lable.setObjectName("learn_mode_lable")
        self.constraction_plans = QtWidgets.QComboBox(self.groupBox_2)
        self.constraction_plans.setGeometry(QtCore.QRect(170, 70, 121, 31))
        self.constraction_plans.setObjectName("constraction_plans")
        self.constraction_plans.addItem("")
        self.constraction_plans.addItem("")
        self.constraction_plans.addItem("")
        self.constraction_plans.addItem("")
        self.constraction_plan_label = QtWidgets.QLabel(self.groupBox_2)
        self.constraction_plan_label.setGeometry(QtCore.QRect(50, 70, 111, 31))
        self.constraction_plan_label.setObjectName("constraction_plan_label")
        self.edu_local = QtWidgets.QComboBox(self.groupBox_2)
        self.edu_local.setGeometry(QtCore.QRect(440, 70, 121, 31))
        self.edu_local.setObjectName("edu_local")
        self.edu_local.addItem("")
        self.edu_local.addItem("")
        self.edu_local.addItem("")
        self.learn_mode = QtWidgets.QComboBox(self.groupBox_2)
        self.learn_mode.setGeometry(QtCore.QRect(170, 20, 121, 31))
        self.learn_mode.setObjectName("learn_mode")
        self.learn_mode.addItem("")
        self.learn_mode.addItem("")
        self.learn_mode.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def indexChange_xuan_ze_men_lei_1(self):
        k = self.xuanze_menlei.currentIndex()

        if k == 2:
            self.xuanze_menlei_2.setVisible(True)
            self.xuanze_menlei_2.setEnabled(True)
            kly = xkml_code()
            kty = kly.get_data()
            show_data_list = [' '.join(i) for i in kty]
            self.xuanze_menlei_2.clear()
            self.xuanze_menlei_2.addItem('选择门类')
            self.xuanze_menlei_2.addItems(show_data_list)
            self.xuanze_menlei_2.setVisible(True)
            self.xuanze_menlei_2.setEnabled(True)

        else:
            self.xuanze_menlei_2.setEnabled(False)
            self.xuanze_menlei_2.setVisible(False)

        self.menlei()

    def indexChange_xuan_ze_men_lei_2(self):
        j = self.xuanze_menlei_2.currentIndex()
        if j <= 0:
            pass
        else:
            self.xuanzexueke.setEnabled(True)
            self.menlei()

    def menlei(self):
        k = self.xuanze_menlei.currentIndex()
        j = self.xuanze_menlei_2.currentIndex()
        if k == 1 or (k == 2 and j != 0):
            self.xuanzexueke.setEnabled(True)
            if k == 1:
                my_xkly_code = xkly_code(dm='zyxw')
                data = my_xkly_code.get_data()
            else:
                rq = self.xuanze_menlei_2.currentText().split(' ')[0]
                my_xkly_code = xkly_code(dm=rq)
                data = my_xkly_code.get_data()

            self.xuanzexueke.clear()
            self.xuanzexueke.addItem('选择学科类别/学科领域')
            self.xuanzexueke.addItems([" ".join(i) for i in data])

        else:
            self.xuanzexueke.setEnabled(False)

    def check(self):
        if self.xuanzexueke.isEnabled():
            if self.xuanzexueke.currentIndex() <= 0:
                QMessageBox.about(MainWindow, "错误选择", "您未选择学科类别或学科领域")
            else:
                return True
        else:
            if self.xuanzexueke.currentIndex() <= 0:
                QMessageBox.about(MainWindow, "错误选择", "请选择学术学位或专业学位")
            else:
                if self.xuanze_menlei_2.isVisible():
                    QMessageBox.about(MainWindow, "错误选择", "您选择了学术学位但未选择门类")

    def dl_click(self):
        self.textBrowser1.clear()
        kks()
        if self.check():
            self.pushButton.setVisible(False)

            data3 = {'地区': choice.c_location(self.edu_local.currentText()),
                     '门类': choice.c_discipline(self.xuanze_menlei.currentText(), self.xuanze_menlei_2.currentText()),
                     '领域': choice.c_field_of_study(self.xuanzexueke.currentText()),
                     '建设计划': choice.c_constraction_plans(self.constraction_plans.currentText()),
                     '学习方式': choice.c_learn_mode(self.learn_mode.currentText())
                     }

            def create_file_name():
                name_1 = self.xuanze_menlei.currentText() + '-' + self.xuanzexueke.currentText()
                name_2 = self.constraction_plans.currentText() + '-' + self.learn_mode.currentText() + '-' + self.edu_local.currentText()
                name = name_1 + '-' + name_2
                return name.replace('不做选择', '').replace('---', '-').replace('--', '-')

            GLOBALS_DICT['file_name'] = create_file_name()

            t1 = threading.Thread(target=t1x, args=(data3,))
            t1.setDaemon(True)

            self.subThread = UpdateThread()
            self.subThread.update_data.connect(self.show_inr)

            t1.start()
            self.subThread.start()

    def show_inr(self, data):
        self.textBrowser1.append(data)
        self.textBrowser1.moveCursor(self.textBrowser1.textCursor().End)
        if data == '下载完成':
            self.pushButton2.setVisible(True)
        if data == '导出完成':
            self.pushButton.setVisible(True)

    def o_c_click(self):
        self.pushButton2.setVisible(False)
        t2 = threading.Thread(target=out_csv, args=tuple())
        t2.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "研招网专业目录下载2022-YanX"))

        self.textBrowser2.setHtml(_translate("MainWindow",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/xx025/YanX\"><img src=\"img/forkme.png\" /></a></p></body></html>"
                                             ))

        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">研招网专业目录下载2022-YanX</span></p></body></html>"))

        self.pushButton.setText(_translate("MainWindow", "开始下载"))
        self.pushButton2.setText(_translate("MainWindow", "导出"))

        self.groupBox.setTitle(_translate("MainWindow", "必选"))
        self.menleileibie_lable.setText(_translate("MainWindow", "门类类别："))
        self.xuanzexueke.setItemText(0, _translate("MainWindow", "选择学科类别/学科领域"))

        self.xuekeleibie_lable.setText(_translate("MainWindow", "学科类别/专业领域："))

        self.groupBox_2.setTitle(_translate("MainWindow", "可选"))
        self.edu_local_lable.setText(_translate("MainWindow", "院校区域："))
        self.learn_mode_lable.setText(_translate("MainWindow", "学习方式:"))
        self.constraction_plans.setItemText(0, _translate("MainWindow", "不做选择"))
        self.constraction_plans.setItemText(1, _translate("MainWindow", "双一流"))
        self.constraction_plans.setItemText(2, _translate("MainWindow", "985"))
        self.constraction_plans.setItemText(3, _translate("MainWindow", "211"))
        self.constraction_plan_label.setText(_translate("MainWindow", "院校建设计划："))
        self.edu_local.setItemText(0, _translate("MainWindow", "不做选择"))
        self.edu_local.setItemText(1, _translate("MainWindow", "A区"))
        self.edu_local.setItemText(2, _translate("MainWindow", "B区"))
        self.learn_mode.setItemText(0, _translate("MainWindow", "不做选择"))
        self.learn_mode.setItemText(1, _translate("MainWindow", "全日制"))
        self.learn_mode.setItemText(2, _translate("MainWindow", "非全日制"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
