import datetime

from _g.g2 import GLOBAL_VAL, G_config, YEAR_VERSION
from _g.g3 import global_queue
from db2 import db_con
from uns import getEdu
from yzw_dl.get_recruit_schools import get_dwmc

'''
下载模块

'''


class dlYzw:

    def __init__(self):
        # 获取数据库连接

        self.__cur = None
        self.__con = None

        self.xia_zai_ren_wu_name = str(GLOBAL_VAL['TASK_NAME'])
        self.xia_zai_ren_wu_id = str(GLOBAL_VAL['TASK_ID'])

        self.zhao_sheng_zhuan_ye = None
        self.kao_shi_fan_wei = None

    def __dl_school(self):
        from yzw_dl.get_recruit_schools import dl_schools
        self.__schools = dl_schools()
        return self.__schools.dl_data()

    def __dl_majors(self, ls):
        from yzw_dl.get_recruit_majors import dl_majors

        rules = [GLOBAL_VAL['gcodes']['院校建设计划'], GLOBAL_VAL['gcodes']['院校区域']]

        ls3 = get_dwmc(rules=rules, ls=ls)

        self.__majors = dl_majors(xue_xiao_lie_biao=ls3)
        self.__majors.set_urls()
        return self.__majors.dl_data()

    #
    def __dl_details(self, ids):
        from yzw_dl.get_major_details import dl_details
        self.__details = dl_details(ids=ids)
        return self.__details.dl_data()

    def store_in_db(self):
        print(datetime.datetime.now())
        self.__con = db_con.get_con()

        self.__cur = self.__con.cursor()

        self.__cur.executemany(
            'insert into 考试范围 (id, tid, political, foreign_language, pro_course_1, pro_course_2) '
            'VALUES (?,?,?,?,?,?)', self.kao_shi_fan_wei)
        self.__cur.executemany(
            'insert into 招生专业 (id, tid, enrollment_unit, examination_method, departments, major, learning_style,'
            ' research_direction, instructor, number_recruit) '
            'VALUES (?,?,?,?,?,?,?,?,?,?)', self.zhao_sheng_zhuan_ye)

        '''
        
        数据库 id 无约束 id+ tid 确保唯一性
        
        '''
        self.__con.commit()
        self.__con.close()
        print(datetime.datetime.now())

    def down_all(self):
        # 下载院校库
        save_year = int(G_config.get('yuanxiaoku')) if G_config.get('yuanxiaoku') else 0
        if YEAR_VERSION > save_year:
            global_queue.put("更新院校库")
            edu2 = getEdu()

            edu2.dl_data()

            G_config['yuanxiaoku'] = YEAR_VERSION
            G_config.write()

            global_queue.put("更新成功")

        self.__add_task()

        ls = self.__dl_school()

        lm = self.__dl_majors(ls=ls)

        d1, d2 = self.__dl_details(ids=lm)
        self.zhao_sheng_zhuan_ye, self.kao_shi_fan_wei = d1, d2

        self.store_in_db()

        self.__ava_task()

        # 关闭数据库连接

    def __add_task(self):
        self.__con = db_con.get_con()

        self.__cur = self.__con.cursor()
        self.__cur.execute('insert into 下载任务(dname, id, available, atime) VALUES  (?,?,0,?)',
                           (self.xia_zai_ren_wu_name, self.xia_zai_ren_wu_id,
                            datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        self.__con.commit()
        self.__con.close()

    def __ava_task(self):
        self.__con = db_con.get_con()
        self.__cur = self.__con.cursor()
        self.__cur.execute('update 下载任务 set available= 1 where id=?', (self.xia_zai_ren_wu_id,))
        self.__con.commit()
        self.__con.close()


def t1x():
    dl_yzw = dlYzw()
    dl_yzw.down_all()

    global_queue.put('下载完成')
