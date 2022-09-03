from queue import Queue

# maxsize默认为0，不受限
# 一旦>0，而消息数又达到限制，q.put()也将阻塞
global_queue = Queue(maxsize=0)

GLOBALS_DICT = {'text_area': None,
                'down_end': False,
                'out_path': None,
                'file_name': ''}
