from PyQt5 import QtWidgets

from ui.static_def import out_date
from ui.ui_action import Ui
from verification import if_star

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui()

    ui.setupUi(MainWindow)

    ui.set_action()
    # 设置按钮相关操作连接
    MainWindow.show()
    # out_date()
    if_star()
    sys.exit(app.exec_())
