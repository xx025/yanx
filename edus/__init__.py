'''
此文件标注 985 大学和 211大学名单，

其中有一些学校名字和参考资料上有些差别做了些如下改动：

    改动：
        国防科学技术大学 --> 国防科技大学
        中国石油大学 --> 中国石油大学(北京),中国石油大学(华东)
        第二军医大学 --> 海军军医大学
        中国地质大学 --> 中国地质大学(武汉),中国地质大学(北京)
        第四军医大学 --> 空军军医大学
        华北电力大学---> 华北电力大学,华北电力大学(保定)

    211 院校供计 115 所
    985 院校共计 39 所
    即使如此可能仍然有错误，所以请慎重

A、B区：https://yzc.hsi.com.cn/kyzx/jybzc/202009/20200904/1972918872.html
211工程名单：http://www.moe.gov.cn/srcsite/A22/s7065/200512/t20051223_82762.html
985工程名单：http://www.moe.gov.cn/srcsite/A22/s7065/200612/t20061206_128833.html

'''
import requests

list985 = ['北京大学', '中国人民大学', '清华大学', '北京航空航天大学', '北京理工大学', '中国农业大学', '北京师范大学',
           '中央民族大学', '南开大学', '天津大学', '大连理工大学', '东北大学', '吉林大学', '哈尔滨工业大学', '复旦大学',
           '同济大学', '上海交通大学', '华东师范大学', '南京大学', '东南大学', '浙江大学', '中国科学技术大学',
           '厦门大学', '山东大学', '中国海洋大学', '武汉大学', '华中科技大学', '湖南大学', '中南大学', '国防科技大学',
           '中山大学', '华南理工大学', '四川大学', '电子科技大学', '重庆大学', '西安交通大学', '西北工业大学',
           '西北农林科技大学', '兰州大学']

list211 = ['北京大学', '中国人民大学', '清华大学', '北京交通大学', '北京工业大学', '北京航空航天大学', '北京理工大学',
           '北京科技大学', '北京化工大学', '北京邮电大学', '中国农业大学', '北京林业大学', '北京中医药大学',
           '北京师范大学', '北京外国语大学', '中国传媒大学', '中央财经大学', '对外经济贸易大学', '北京体育大学',
           '中央音乐学院', '中央民族大学', '中国政法大学', '华北电力大学', '华北电力大学(保定)', '南开大学', '天津大学',
           '天津医科大学',
           '河北工业大学', '太原理工大学', '内蒙古大学', '辽宁大学', '大连理工大学', '东北大学', '大连海事大学',
           '吉林大学', '延边大学', '东北师范大学', '哈尔滨工业大学', '哈尔滨工程大学', '东北农业大学', '东北林业大学',
           '复旦大学', '同济大学', '上海交通大学', '华东理工大学', '东华大学', '华东师范大学', '上海外国语大学',
           '上海财经大学', '上海大学', '海军军医大学', '南京大学', '苏州大学', '东南大学', '南京航空航天大学',
           '南京理工大学', '中国矿业大学', '河海大学', '江南大学', '南京农业大学', '中国药科大学', '南京师范大学',
           '浙江大学', '安徽大学', '中国科学技术大学', '合肥工业大学', '厦门大学', '福州大学', '南昌大学', '山东大学',
           '中国海洋大学', '中国石油大学(北京)', '中国石油大学(华东)', '郑州大学', '武汉大学', '华中科技大学',
           '中国地质大学(武汉)', '中国地质大学(北京)', '武汉理工大学', '华中农业大学', '华中师范大学',
           '中南财经政法大学', '湖南大学', '中南大学', '湖南师范大学', '国防科技大学', '中山大学', '暨南大学',
           '华南理工大学', '华南师范大学', '广西大学', '海南大学', '四川大学', '西南交通大学', '电子科技大学',
           '四川农业大学', '西南财经大学', '重庆大学', '西南大学', '贵州大学', '云南大学', '西藏大学', '西北大学',
           '西安交通大学', '西北工业大学', '西安电子科技大学', '长安大学', '西北农林科技大学', '陕西师范大学',
           '空军军医大学', '兰州大学', '青海大学', '宁夏大学', '新疆大学', '石河子大学']

loc_A = ['北京', '天津', '河北', '山西', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西',
         '山东', '河南', '湖北', '湖南', '广东', '重庆', '四川', '陕西']

loc_B = ['内蒙古', '广西', '海南', '贵州', '云南', '西藏', '甘肃', '青海', '宁夏', '新疆']

from bs4 import BeautifulSoup

from db import con, cur


class edu:
    def __init__(self, name, is11, loc, lishu, yjsy, zzhx):
        self.name = name
        self.is11 = is11
        self.is985 = 1 if name in list985 else 0
        self.is211 = 1 if name in list211 else 0
        self.locAB = 'B' if loc in loc_B else 'A'
        self.loc = loc
        self.lishu = lishu
        self.yjsy = yjsy
        self.zzhx = zzhx

    def info(self):
        return (self.name,
                self.is11,
                self.is985,
                self.is211,
                self.locAB,
                self.loc,
                self.lishu,
                self.yjsy,
                self.zzhx)


class getEdu:
    def __init__(self):
        self.url = 'https://yz.chsi.com.cn/sch/'
        self.data = []
        self.l_B = loc_B
        self.l_A = loc_A
        self.list211 = list211
        self.list985 = list985
        self.start = 0

    def __req_data(self):
        while True:
            page_text = requests.get(url=self.url, params={'start': self.start}).text
            soup = BeautifulSoup(page_text)
            if soup.select('.yxk-table table tbody tr').__len__() == 1 and soup.select_one(
                    '.yxk-table table .noResult'):
                break
            else:
                self.start += 20
                print('下一页')
            for i in soup.select('.yxk-table table tbody tr'):
                name = i.select('td')[0].select_one('a').text.strip()
                is11 = 1 if i.select('td')[0].select_one('span') else 0
                loc = i.select('td')[1].text
                lishu = i.select('td')[2].text
                yjsy = 1 if i.select('td')[3].select_one('i') is None else 0
                zzhx = 1 if i.select('td')[4].select_one('i') is None else 0

                newedu = edu(name=name,
                             is11=is11,
                             loc=loc,
                             lishu=lishu,
                             yjsy=yjsy,
                             zzhx=zzhx)
                self.data.append(newedu.info())
        self.__store_in_db()

    def __store_in_db(self):
        cur.execute('DELETE FROM edus')
        cur.executemany(
            'INSERT INTO edus(name, is11, is985, is211,locAB, loc, lishu, yjsy, zzhx)'
            'VALUES (?,?,?,?,?,?,?,?,?)', self.data)
        con.commit()

    def get_data(self):
        cursor = cur.execute("SELECT *  FROM edus")
        data = [i for i in cursor]
        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data


use2 = getEdu()
use2.get_data()
