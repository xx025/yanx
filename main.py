from get_recruit_edu import get_zsyx
from show_def import xuanzediqu, xuanzemenlei, xuanzelingyu, xuanzezhuanye, xuenzexuexifangshi

print('''
欢迎使用研招网爬虫2022

爬虫功能：
    1. 采集你所提供条件下的研招网所有考试院校的招生专业数据，
    2. 另外还提供以下附加数据和条件：
        1. 学校是A区院校或B区院校
        2. 学校是双一流院校或985或211院校

如下 清华大学 计算机科学与技术专业招生，
院校地区：   A区
院校隶属：   双一流、985、211 
招生单位：	(10003)清华大学	
考试方式：	统考
院系所：	(024)计算机科学与技术系	
专业：	(081200)计算机科学与技术
学习方式：	全日制	
研究方向：	(03)计算机应用技术
指导老师：	不区分导师	
拟招人数：	专业：12(不含推免)
备注：	招生人数后续可能调整，请关注清华研招网（http://yz.tsinghua.edu.cn）公布的招生专业目录
考试范围：政治	      (101)思想政治理论           见招生简章
        外语	      (201)英语（一）             见招生简章
        业务课一    (301)数学（一）             见招生简章
        业务课二    (912)计算机专业基础综合       见招生简章       

GITHUB地址：https://github.com/xx025/yzw-spider
=================================================================
''')

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

data = dl_zsyx.req_data()
