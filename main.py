import os

from user import user


def show_welcome():
    os.system('cls')
    print('''
    爬虫功能：
        1. 采集你所提供条件下的研招网所有考试院校的招生专业数据，
        2. 另外还提供以下附加数据和条件：
            1. 学校是A区院校或B区院校
            2. 学校是双一流院校或985或211院校

    在正式开始之前，将需要问你几个问题作
    ''')
    input('回车继续')


show_welcome()

user1 = user()

user1.set_discipline()
# 选择学科门类，如 学硕 08 工学 或 专硕

user1.set_field_of_study()
# 选择专业领域 ，如 学硕 0812 计算机科学与技术

user1.set_major()
# 选择具体专业，如 大数据科学与工程

user1.set_learn_way()
# 选择学习方式，如 全日制 或 非全

user1.set_location()
# 选择地区 如 北京

user1.set_construction_plans()
# 选择学校建设计划 如 双一流11

'''user1.set_user_choice_items(location_codes=None,
                            discipline_code='05',
                            field_of_study_code='0501',
                            majors=None,
                            learn_mode=None,
                            construction_plans={'211': '0', '985': '0', '11': '0'})'''

user1.dl_schools()
# 下载学校信息

user1.dl_majors()
# 下载专业信息


user1.dl_details()
# 下载具体招生考试科目人数等
