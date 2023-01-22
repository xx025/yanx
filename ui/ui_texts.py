# 这个文件内包含程序界面文字和外链内容
from _g import REAL_PATH
from stools.sk2 import get_year, gta

version = {'v': 'v3.1.22',
           'id': "20230122"}
version_build = version.get('v')
# 软件的版本，每次构建时更改,显示在标题栏


version_id = version.get('id')
# 用于更新和检查
project_name = 'YanX'

year = get_year()
# 年份根据据研招网（https://yz.chsi.com.cn/zsml/zyfx_search.jsp）动态生产

WIN_TITLE = win_title = '{}-研招网硕士专业目录下载-{}'.format(project_name, version_build)
# 窗体的标题


TITLE = title = '研招网{}年硕士专业目录下载'.format(year)
PIC_PATH = pic_path = REAL_PATH + '\db\githubstar3.png'

GITHUB_URL = github_url = 'https://github.com/xx025/YanX'
GITHUB_URL2 = 'https://github.com/xx025/YanX-Docs#%E6%AD%A4%E4%BB%93%E5%BA%93%E8%B4%A1%E7%8C%AE%E8%80%85'
GITHUBPAGE3 = 'https://xx025.github.io/YanX/'
DL_BAN = "为了防止滥用，软件限制了下载次数，您看到此弹窗意味着，您已经下载了过多的次数；你现在只能导出你下载的文档，谢谢！"

UPLOAD_TIPS = "亲爱的，你的目录导出文件存储在桌面上了！"

info = gta()
BULLETIN_BOARD = info.get('tips_mes')
# 公告栏
XMLL = info['welcome_mes'].get('title')
WSXM = info['welcome_mes'].get('content')
UPDATE = update = info.get('update')
