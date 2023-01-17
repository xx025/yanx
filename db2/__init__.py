import sqlite3

import numpy
import numpy as np

from _g import REAL_PATH


def get_dqdm():
    con = db_con.get_con()
    cur = con.cursor()
    re = cur.execute('select dm,mc,ab from 地区代码')
    list11 = [i for i in re]
    con.close()

    return list11


def get_uis11_list():
    con = db_con.get_con()
    cur = con.cursor()
    re = cur.execute('select 院校名称 from 院校库 where 双一流==1')
    list11 = [i[0] for i in re]
    con.close()

    return list11


def get_abquy(ab):
    con = db_con.get_con()
    cur = con.cursor()
    re = cur.execute(f'select dm from 地区代码 where ab=?', [ab])
    list11 = [i[0] for i in re]
    con.close()

    return list11


class db_con:

    @staticmethod
    def get_con():
        con = sqlite3.connect(REAL_PATH + '\db\database.db', check_same_thread=False)
        return con


def get_down_task():
    con = db_con.get_con()
    cur = con.cursor()
    c = cur.execute("select dname||'-'||atime,id from 下载任务 where available = 1;")
    # GLOBAL_VAL['DOWN_TASK'] = [k for k in c]

    result = {}
    for key, value in c:
        result[key] = value
    con.close()

    return result


def daochu_xinxi(tids):
    con = db_con.get_con()

    d1 = []

    max_length = 0
    table_title = ['学校', '所在地', 'AB区', '所属', '院校建设',
                   '考试方式', '院系所', '专业',
                   '学习方式', '研究方向', '指导老师',
                   '拟招人数', '政治', '外语', '业务课1', '业务课2']
    d1.append(table_title)
    sql = f'select id from 招生专业 where tid=?'
    for tid in tids:
        ids = [id[0] for id in con.execute(sql, (tid,))]
        for id in ids:
            data = [None, None, None, None, None]
            sql1 = 'select 所在地,AB,院校隶属,IS985,IS211,双一流 from 院校库 where 院校代码 = ?'
            data5 = []
            dats2 = list([k for k in con.execute(sql1, ((id[:5]),))][0])

            data5.append(dats2[0])
            data5.append(f'{dats2[1]}区')
            data5.append(dats2[2])

            if '1' not in dats2[3:]:
                data5.append('普通院校')
            else:
                data5.append(
                    f"{'985,' if dats2[3] == '1' else ''}{'211,' if dats2[4] == '1' else ''}{'双一流' if dats2[5] == '1' else ''}")

            data[1:] = data5[:]
            sql3 = 'select enrollment_unit,examination_method,departments,major,learning_style,research_direction,instructor,number_recruit from 招生专业 where id=? and tid= ?'
            xueXiaoXinXi = list([k for k in con.execute(sql3, (id, tid))][0])

            data[0] = xueXiaoXinXi[0]

            data.extend(xueXiaoXinXi[1:])
            sql2 = 'select political,foreign_language,pro_course_1,pro_course_2 from 考试范围 where id=? and tid=? '

            for k in con.execute(sql2, (id, tid)):
                data.extend(k)

            if len(data) > max_length:
                max_length = len(data)
            d1.append(data)
    else:
        con.close()

    for i in range(len(d1)):

        if len(d1[i]) < max_length:
            d1[i].extend(['-' for _ in range(max_length - len(d1[i]))])

    d1 = np.array(d1, dtype=str)

    # d1 = np.delete(d1, [0, 1, 2, 3], axis=1)

    return d1
