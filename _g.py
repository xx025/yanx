import os
from queue import Queue

from configobj import ConfigObj

# maxsize默认为0，不受限
# 一旦>0，而消息数又达到限制，q.put()也将阻塞
global_queue = Queue(maxsize=0)

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
