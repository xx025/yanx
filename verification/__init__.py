import json
import sys
import winreg

import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit

from _g import G_config
from ui.static_def import opurl
from ui.ui_texts import GITHUB_URL, XMLL, WSXM


# github star检查
def if_star(content=GITHUB_URL, op_e=True):
    saved_id = G_config.get('github_id')

    # 保存的id

    def check_val(val):
        try:
            res = requests.get(f'https://api.github.com/users/{val}/starred?per_page=1', timeout=4, verify=False).text
            res = json.loads(res)
            for i in res:
                html_url = i.get('owner').get('html_url') + '/' + i.get('name')
                # print(html_url)
                if GITHUB_URL == html_url:
                    return True
            else:
                return False
        except Exception:
            return False

    if saved_id and check_val(saved_id):
        # 存在保存的id 而且检查通过
        pass
    else:
        # 检查不通过 或 不存在保存的id
        value, ok = QInputDialog.getText(QtWidgets.QMainWindow(), XMLL, WSXM, QLineEdit.Normal,
                                         content)

        if ok:
            G_config['github_id'] = value
            G_config.write()
            if op_e:
                # 只弹出一次浏览器
                opurl(GITHUB_URL)
            if_star(content=value, op_e=False)
        else:
            sys.exit()


# 注册表记录

reg_path = r'.DEFAULT\Software\yanx6666521'


def get_dls():
    try:
        winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, reg_path, reserved=0, access=winreg.KEY_WRITE)
    finally:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    try:
        winreg.QueryValueEx(key, "dls")
    except FileNotFoundError as e:
        winreg.SetValueEx(key, 'dls', 0, winreg.REG_SZ, '0')
    finally:
        val, type3 = winreg.QueryValueEx(key, "dls")
        key.Close()
        # print(val)
    return int(val)


def add_dls():
    try:
        winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, reg_path, reserved=0, access=winreg.KEY_WRITE)
    finally:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    try:
        winreg.QueryValueEx(key, "dls")
    except FileNotFoundError as e:
        winreg.SetValueEx(key, 'dls', 0, winreg.REG_SZ, '0')
    finally:
        val, type3 = winreg.QueryValueEx(key, "dls")
        winreg.SetValueEx(key, 'dls', 0, winreg.REG_SZ, str(int(val) + 1))
        key.Close()

    return int(val)
