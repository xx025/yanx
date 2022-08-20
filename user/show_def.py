import os


def show_welcome():
    os.system('cls')
    print('''
    欢迎使用研招网招生信息爬虫2022

    爬虫功能：
        1. 采集你所提供条件下的研招网所有考试院校的招生专业数据，
        2. 另外还提供以下附加数据和条件：
            1. 学校是A区院校或B区院校
            2. 学校是双一流院校或985或211院校
   

    GITHUB地址：https://github.com/xx025/yzw-spider
    ''')
    input('回车继续')
    os.system('cls')



