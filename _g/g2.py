import os

from configobj import ConfigObj

from stools.sk4 import get_year

REAL_PATH = os.getcwd()

# 配置文件
setting_path = os.path.join(REAL_PATH, 'setting.cfg')

G_config = ConfigObj(setting_path, encoding='UTF-8')

# 当前下载任务参数

# 關於下載任務的全局變量
GLOBAL_VAL = dict()

# MAX_SCOPE : 最大行數
# TASK_ID : 當前任務的ID
# TASK_NAME : 任務的名字

GLOBAL_VAL['MAX_SCOPE'] = 0

GLOBAL_VAL['TASK_NAME'] = ''
GLOBAL_VAL['TASK_ID'] = ''

GLOBAL_VAL['DOWN_TASK'] = None

GLOBAL_VAL['gcodes'] = {}

GLOBAL_VAL['TASK_SELECTED'] = {'ids': [], 'texts': []}
YEAR_VERSION= get_year()
version = {'v': 'v3.2.23',
           'id': "20230223"}
