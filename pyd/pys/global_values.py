from queue import Queue

# maxsize默认为0，不受限
# 一旦>0，而消息数又达到限制，q.put()也将阻塞
global_queue = Queue(maxsize=0)

GLOBALS_DICT = {'text_area': None,
                'down_end': False,
                'out_path': None,
                'file_name': '',
                'MAX_SCOPE': 0}


UPLOAD_TIPS = "亲爱的，你的目录下载完了！；你是否愿意将您下载的目录上传到 GitHub 仓库 以帮助更多的同学？ (这不会占用你太多时间，在你上传后，将被列入YanX-Docs 这个仓库贡献者名单)"
YAN_X_DOCS_URL = 'https://github.com/xx025/YanX-Docs#提交步骤'
MainTitle = 'YanX-研招网专业目录下载-{}'.format('2023')
WindowTitle = MainTitle + '-v0.1.{}.{}'.format(9, 16)
