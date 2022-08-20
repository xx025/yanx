import os

from show_def import show_welcome
from user import user

show_welcome()

print('''在爬虫运行之前，将需要问你几个问题作为爬虫爬取条件''')

use1 = user()

diqu = use1.xuanzediqu()
# 选择地区 如 北京
a = input('回车继续')
os.system('cls')

xkml = use1.xuanzemenlei()
# 选择学科门类，如 学硕 08 工学 或 专硕
a = input('回车继续')
os.system('cls')


xkly = use1.xuanzelingyu(xkml)
# 选择专业领域 ，如 学硕 0812 计算机科学与技术 或 专硕 0854 电子信息
a = input('回车继续')
os.system('cls')


zyn = use1.xuanzezhuanye(xkly)
# 选择具体专业，如 大数据科学与工程
a = input('回车继续')
os.system('cls')


xxfs = use1.xuenzexuexifangshi()
# 选择学习方式，如 全日制 或 非全

# dl_zsyx = get_zsyx(mldm=xkml, yjxkm=xkly, ssdm=diqu, zymc=zyn, xxfs=xxfs)
#
# data = dl_zsyx.get_data()
# # 获取到招生院校，进一步可筛选 双一流、985、211 和地区相关条件
# # 再下一步 将获取院校里的专业
