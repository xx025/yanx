from get_recruit_edu import get_zsyx
from show_def import xuanzediqu, xuanzemenlei, xuanzelingyu, xuanzezhuanye, xuenzexuexifangshi, show_welcome

show_welcome()

print('''在爬虫运行之前，将需要问你几个问题作为爬虫爬取条件''')
diqu = xuanzediqu()
# 选择地区 如 北京
xkml = xuanzemenlei()
# 选择学科门类，如 学硕 08 工学 或 专硕
xkly = xuanzelingyu(xkml)
# 选择专业领域 ，如 学硕 0812 计算机科学与技术 或 专硕 0854 电子信息
zyn = xuanzezhuanye(xkly)
# 选择具体专业，如 大数据科学与工程
xxfs = xuenzexuexifangshi()
# 选择学习方式，如 全日制 或 非全

dl_zsyx = get_zsyx(mldm=xkml, yjxkm=xkly, ssdm=diqu, zymc=zyn, xxfs=xxfs)

data = dl_zsyx.get_data()
# 获取到招生院校，进一步可筛选 双一流、985、211 和地区相关条件
# 再下一步 将获取院校里的专业
