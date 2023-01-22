import ctypes
import os
import threading

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QDialog, QLabel

from _g import global_queue, GLOBAL_VAL, REAL_PATH
from db2 import get_down_task
from task.dls import dao_chu_ren_wu, shan_chu_ren_wu
from ui.static_def import UpdateThread
from ui.ui_texts import UPLOAD_TIPS, DL_BAN
from ui.ui_window import Ui_MainWindow
from verification import get_dls, add_dls
from yzw_dl import t1x
from zyfx_search import g_params, g_params_def


class Ui(Ui_MainWindow):
    def __init__(self):

        self.lv_selected = None
        self.xueWeiLeiBieBoxOk = False
        self.menLeiLeiBieBoxOk = False
        self.xueKeLeiBieBoxOk = False

        self.init_set()

    def set_action(self):

        self.zhuanYeMingChengBox.setDisabled(True)

        self.subThread = UpdateThread()
        self.subThread.update_data.connect(self.show_inr)
        self.subThread.start()
        # 开启监听队列消息
        self.update_list_v()
        # 更新下载任务视图

        self.menLeiLeiBieBox.setDisabled(True)
        self.xueKeLeiBieBox.setDisabled(True)
        # 设置门类类别和学科类别禁用，需要等到上一级选择后才启用
        self.kaiShiXiaZaiBtn.setDisabled(True)
        # 设置开始下载按钮禁用，只有必选项全部正确选择后才启用

        self.daoChuSheZhi.setVisible(False)
        # 向输出结果框添加测试数据

        self.listView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listView.setStyleSheet("background-color:#f0f0f0;outline:none;")
        # 设置表格可以多选

        self.xueWeiLeiBieBox.currentTextChanged.connect(self.xue_wei_lei_bie_xuan_ze)
        self.menLeiLeiBieBox.currentTextChanged.connect(self.men_lei_lei_bie_xuan_ze)
        self.xueKeLeiBieBox.currentTextChanged.connect(self.xue_ke_lie_bie_xuan_ze)
        # 设置必选选择框关联

        self.kaiShiXiaZaiBtn.clicked.connect(self.kai_shi_xia_zai)
        # 点击开始下载

        self.quXiaoXiaZaiBtn.setDisabled(True)

        self.listView.clicked.connect(self.list_v_update_selected)
        self.quXiaoXiaZaiBtn.clicked.connect(self.stop_xia_zai_xian_cheng)

        self.daoChu.setDisabled(True)
        self.shanChuXuanZhongBtn.setDisabled(True)
        # 设置导出按钮禁用，启动程序时没有任何选择
        # 设置删除按钮禁用
        # 按钮的重新启用，在list_v_update_selected() 中更新

        self.daoChu.clicked.connect(lambda: dao_chu_ren_wu())

        # self.daoChuSheZhi.clicked.connect(lambda: dao_chu_ren_wu(data=self.lv_selected, param=1))

        self.shanChuXuanZhongBtn.clicked.connect(
            lambda: (shan_chu_ren_wu(), self.update_list_v()))

        self.daoChu.setToolTip(
            '将选中的下载任务导出，如果选中多个则将多个任务合并导出到一个文件，如可以将专硕和学硕两次下载任务合并导出')
        self.daoChuSheZhi.setToolTip('设置导出数据的内容列')

        self.kaiShiXiaZaiBtn.setToolTip('开始下载，请勿滥用软件')
        self.shanChuXuanZhongBtn.setToolTip('将选中的任务删除')

        self.yuanXiaoJianSheJiHuaBox.addItems(g_params['院校建设计划']['items'])
        self.xueXIFangShiBox.addItems(g_params['学习方式']['items'])
        self.yuanXiaoQuYuBox.addItems(g_params['院校区域']['items'])

        # 设置打赏

        self.daShangBtn.clicked.connect(self.daShang)

    def list_v_update_selected(self):
        # 更新选中任务序号
        selected = self.listView.selectedIndexes()

        # python 3.6+ 字典是有序的
        # 可用选择序号推算出 选择的项目

        selected_ids = []

        selected_texts = []
        all_keys = list(GLOBAL_VAL['DOWN_TASK'].keys())
        for selectedIndex in selected:
            selected_key = all_keys[selectedIndex.row()]
            selected_texts.append(selected_key)
            selected_ids.append(GLOBAL_VAL['DOWN_TASK'][selected_key])

        GLOBAL_VAL['TASK_SELECTED']['ids'] = selected_ids
        GLOBAL_VAL['TASK_SELECTED']['texts'] = selected_texts

        # 将选中的数据同步到全局变量

        count_selected = selected.__len__()
        if count_selected >= 1:
            self.daoChu.setDisabled(False)
            self.shanChuXuanZhongBtn.setDisabled(False)
        else:
            self.shanChuXuanZhongBtn.setDisabled(True)
            self.daoChu.setDisabled(True)

    def init_set(self):
        self.menLeiLeiBieBoxOk = False
        self.xueKeLeiBieBoxOk = False

    def re_set(self):

        # 重新设置按钮和选择框状态
        uk0 = self.xueWeiLeiBieBoxOk
        uk1 = self.menLeiLeiBieBoxOk
        uk2 = self.xueKeLeiBieBoxOk

        if not uk0:
            uk1 = False
        if not uk1:
            uk2 = False
        # 控制选择框和按钮的可用性
        self.menLeiLeiBieBox.setDisabled(not uk0)
        self.xueKeLeiBieBox.setDisabled(not uk1)

        self.kaiShiXiaZaiBtn.setDisabled(not (uk0 and uk1 and uk2))

    def xue_wei_lei_bie_xuan_ze(self):

        self.init_set()

        self.menLeiLeiBieBox.clear()
        self.menLeiLeiBieBox.addItem('请选择')

        def f1():
            xwlb_text = self.xueWeiLeiBieBox.currentText()
            if xwlb_text in g_params['学位类别']['items']:
                g_params['学位类别']['selected'] = xwlb_text
                # 设置选择的学位类别
                g_params_def.update_mllb()
                # 根据对应的学位类别更新门类类别
                self.menLeiLeiBieBox.addItems(g_params['门类类别']['items'])
                # 添加门类类别
                self.xueWeiLeiBieBoxOk = True
            else:
                self.xueWeiLeiBieBoxOk = False
            self.re_set()
            # 重新设置状态

        t1 = threading.Thread(target=f1, args=tuple())
        t1.setDaemon(True)
        t1.start()

    def men_lei_lei_bie_xuan_ze(self):

        self.xueKeLeiBieBox.clear()
        self.xueKeLeiBieBox.addItem('请选择')

        def f1():
            xwlb_text = self.menLeiLeiBieBox.currentText()

            if xwlb_text in g_params['门类类别']['items']:

                g_params['门类类别']['selected'] = xwlb_text
                g_params_def.update_xklb()
                self.xueKeLeiBieBox.addItems(g_params['学科类别']['items'])

                self.menLeiLeiBieBoxOk = True
            else:
                self.menLeiLeiBieBoxOk = False
            self.re_set()
            # 重新设置状态

        t1 = threading.Thread(target=f1, args=tuple())
        t1.setDaemon(True)
        t1.start()

    def xue_ke_lie_bie_xuan_ze(self):

        self.zhuanYeMingChengBox.clear()
        self.zhuanYeMingChengBox.addItem('不做选择')

        def f1():

            xklb_text = self.xueKeLeiBieBox.currentText()

            if xklb_text in g_params['学科类别']['items']:

                g_params['学科类别']['selected'] = xklb_text

                g_params_def.update_zymc()

                self.zhuanYeMingChengBox.addItems(g_params['专业名称']['items'])

                self.zhuanYeMingChengBox.setDisabled(False)

                self.xueKeLeiBieBoxOk = True
            else:
                self.xueKeLeiBieBoxOk = False
            self.re_set()

        t1 = threading.Thread(target=f1, args=tuple())
        t1.setDaemon(True)
        t1.start()

    def stop_xia_zai_xian_cheng(self):
        global_queue.put("取消下载")

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.t1.ident,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.t1.ident, 0)
            print('Exception raise failure')

    def kai_shi_xia_zai(self):

        # 点击开始下载更新可选择参数到g_parma

        if get_dls() < 10:

            ghd = list()

            ghd.append(self.menLeiLeiBieBox.currentText())
            ghd.append(self.xueKeLeiBieBox.currentText())
            ghd.append(self.zhuanYeMingChengBox.currentText())
            ghd.append(self.xueXIFangShiBox.currentText())
            ghd.append(self.yuanXiaoJianSheJiHuaBox.currentText())
            ghd.append(self.yuanXiaoQuYuBox.currentText())

            l2 = list()
            for i in range(len(ghd)):
                if ghd[i] != '不做选择':
                    l2.append(ghd[i])

            import uuid

            GLOBAL_VAL['TASK_NAME'] = '-'.join(l2)
            GLOBAL_VAL['TASK_ID'] = uuid.uuid1()

            GLOBAL_VAL['gcodes'] = {
                '门类代码': g_params['门类类别']['items'][self.menLeiLeiBieBox.currentText()],
                '学科代码': g_params['学科类别']['items'][self.xueKeLeiBieBox.currentText()],
                '专业名称': g_params['专业名称']['items'].get(self.zhuanYeMingChengBox.currentText(), ''),
                '学习方式': g_params['学习方式']['items'][self.xueXIFangShiBox.currentText()],
                '院校建设计划': g_params['院校建设计划']['items'][self.yuanXiaoJianSheJiHuaBox.currentText()],
                '院校区域': g_params['院校区域']['items'][self.yuanXiaoQuYuBox.currentText()]
            }
            self.kaiShiXiaZaiBtn.setDisabled(True)
            self.quXiaoXiaZaiBtn.setDisabled(False)

            self.xiaZaiYuanXiaoXinXiProgressBar.setValue(0)

            self.xiaZaiZhuanYeXinXiProgressBar.setValue(0)

            self.xiaZaiKaoShiXinXiProgressBar.setValue(0)

            self.t1 = threading.Thread(target=t1x, args=tuple())
            self.t1.setDaemon(True)
            self.t1.start()
        else:
            # 触发滥用
            QMessageBox.critical(QtWidgets.QMainWindow(), "警告！",
                                 DL_BAN,
                                 QMessageBox.Yes)

    def update_list_v(self):

        GLOBAL_VAL['DOWN_TASK'] = get_down_task()

        task_list2 = list(GLOBAL_VAL['DOWN_TASK'].keys())

        slm = QStringListModel()
        slm.setStringList(task_list2)
        self.listView.setModel(slm)

        self.list_v_update_selected()

    def show_inr(self, data):
        stype = None
        try:
            data: dict = eval(data)
            stype = data.get('type')
        except Exception:
            pass

        if stype:
            val = data.get('val')
            dels = data.get('text')
            if stype == '学校':
                self.xiaZaiYuanXiaoXinXiProgressBar.setValue(val)
            elif stype == '专业':
                self.xiaZaiZhuanYeXinXiProgressBar.setValue(val)

            elif stype == '考试':
                self.xiaZaiKaoShiXinXiProgressBar.setValue(val)

            self.dangQianRenWuLable.setText(dels)
        else:

            if data == "取消下载" or data == "下载完成":
                self.quXiaoXiaZaiBtn.setDisabled(True)
                self.kaiShiXiaZaiBtn.setDisabled(False)

            if data == "下载完成":
                self.update_list_v()
                add_dls()
            if data == '开始导出':
                print(data)
                self.daoChu.setDisabled(True)

            if data == '导出完成':
                self.daoChu.setDisabled(False)
                # 后两项分别为按钮(以|隔开，共有7种按钮类型，见示例后)、默认按钮(省略则默认为第一个按钮)
                QMessageBox.question(QtWidgets.QMainWindow(), "导出完成",
                                     UPLOAD_TIPS, QMessageBox.Yes)
            self.dangQianRenWuLable.setText(str(data))

    def daShang(self):

        dialog_fault = QDialog()

        image_path = os.path.join(REAL_PATH, "db\dashang.png")

        dialog_fault.setWindowTitle('💴打赏')
        print(image_path)
        pic = QPixmap(image_path)
        label_pic = QLabel("show", dialog_fault)
        label_pic.setPixmap(pic)
        label_pic.setGeometry(10, 10, 443, 708)

        dashangText = QtWidgets.QLabel(dialog_fault)
        dashangText.setWordWrap(True)
        dashangText.setGeometry(QtCore.QRect(10, 10, 440, 81))
        font = QtGui.QFont()
        font.setPointSize(14)
        dashangText.setFont(font)
        dashangText.setText('北方的农村没有暖气和空调，我在很多个寒冷的深夜里开发它，包括现在，感谢你的支持！')
        dialog_fault.exec_()
