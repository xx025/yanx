import csv
import datetime
import winreg

from pyd.db import db_con
from pyd.pys.global_values import GLOBALS_DICT, global_queue


# https://www.jb51.net/article/181007.htm
# CSV文件输出乱码问题
# Sqlite 字符串截取 substr https://www.techonthenet.com/sqlite/functions/substr.php


class School:

    def __init__(self, data):
        self.data = data
        self.院校名称 = data[1]
        self.所在地 = data[2]
        self.AB区 = data[3]
        self.院校建设计划 = self.contraction()
        self.考试方式 = data[7]
        self.学院 = data[8]
        self.专业 = data[9]
        self.学习方式 = data[10]
        self.招生人数 = data[11]

    def contraction(self):
        uis = []
        if self.data[4] == '1':
            uis.append('985')
        if self.data[5] == '1':
            uis.append('211')
        if self.data[6] == '1':
            uis.append('双一流')
        if len(uis) == 0:
            return '普通院校'
        else:
            return '，'.join(uis)

    def get_data(self):
        return [self.院校名称, self.所在地, self.AB区, self.院校建设计划, self.考试方式, self.学院, self.专业,
                self.学习方式, self.招生人数]


class MajorsScopes:

    def __init__(self):

        self.con = db_con.get_con()
        self.data = self.scope_d()
        self.con.close()

    def query_school_data(self):
        sql = '''
        select 招生专业.id, 院校库.院校名称,院校库.所在地,院校库.AB,院校库.IS985,院校库.IS211,
           院校库.双一流,招生专业.examination_method,招生专业.departments,招生专业.major,
           招生专业.learning_style,招生专业.number_recruit FROM 招生专业,院校库
        where substr(招生专业.id, 0, 6) == 院校库.院校代码'''

        # SQL 查询语句
        return [i for i in self.con.execute(sql)]
        # 返回查询结果

    def query_scope_data(self, id):
        dts = []
        sql = '''select * from 考试范围 where id=?'''
        [dts.extend(i[1:]) for i in self.con.execute(sql, (id,))]
        return dts

    def scope_d(self):
        d0 = []

        data1 = self.query_school_data()
        # 向数据库查询

        for i in data1:
            d1 = School(i)
            row1 = d1.get_data()
            row1.extend(self.query_scope_data(i[0]))
            if len(row1) > GLOBALS_DICT['MAX_SCOPE']:
                # 记录最大附带考试科目每一行的最大长度，优化CSV
                GLOBALS_DICT['MAX_SCOPE'] = len(row1)
            d0.append(row1)
        return d0

    def get_data(self):
        return self.data


def out_csv():
    now = datetime.datetime.now()

    path = desktop_path() + r'\{}-{}-{}.csv'.format(GLOBALS_DICT['file_name'], now.date(), now.second)
    path = str(path).replace(' ', '').replace('---', '-').replace('--', '-')

    with open(path, 'a', encoding='utf-8-sig', newline="") as f:
        writer = csv.writer(f)

        d1 = MajorsScopes()
        data = d1.get_data()
        head = ['学校', '所在地', 'AB区', '院校建设计划', '考试方式', '学院', '专业', '学习方式',
                '招生人数', '政治考试', '外语考试',
                '专业课1考试', '专业课二考试']

        maxLen = GLOBALS_DICT['MAX_SCOPE']
        if maxLen > len(head):
            for i in range(maxLen - len(head)):
                head.append("-")

        writer.writerow(head)
        for i in data:
            if maxLen > len(i):
                for k in range(maxLen - len(i)):
                    i.extend('-')
            writer.writerow(i)

    GLOBALS_DICT['out_path'] = path
    global_queue.put('导出完成')
    global_queue.put('导出目录' + GLOBALS_DICT['out_path'])


def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path
