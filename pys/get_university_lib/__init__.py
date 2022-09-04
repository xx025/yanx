
import requests

from pys.processing_string import get_url_param

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

from pys.db import db_con


class edu:
    def __init__(self, 院校名称, 所在地, 双一流, 院校隶属, 研究生院, 自主划线, 院校代码):
        self.院校名称 = 院校名称
        self.双一流 = 双一流
        self.所在地 = 所在地
        self.院校隶属 = 院校隶属
        self.研究生院 = 研究生院
        self.自主划线 = 自主划线
        self.院校代码 = 院校代码
        self.IS985 = 1 if 院校名称 in list985 else 0
        self.IS211 = 1 if 院校名称 in list211 else 0
        self.AB = 'B' if 所在地 in loc_B else 'A'

    def info(self):
        return (
            self.院校名称, self.所在地, self.院校隶属, self.研究生院, self.自主划线, self.院校代码, self.IS985,
            self.IS211, self.AB, self.双一流)


class getEdu:
    def __init__(self):
        self.链接 = 'https://yz.chsi.com.cn/sch/search.do'
        self.数据 = []
        self.页码 = 0
        # 初始页面设置为0

    def __req_data(self):
        while True:
            print(self.页码)
            page_text = requests.get(url=self.链接, params={'start': self.页码}).text
            soup = BeautifulSoup(page_text, "html.parser")
            if soup.select('.yxk-table table tbody tr').__len__() == 1 and soup.select_one(
                    '.yxk-table table .noResult'):
                break
            else:
                us_list = soup.select('.yxk-table table tbody tr')
                self.页码 = len(us_list) + self.页码
                tmp_data = []
                for i in us_list:
                    院校名称 = i.select('td')[0].select_one('a').text.strip()
                    双一流 = 1 if i.select('td')[0].select_one('span') else 0
                    所在地 = i.select('td')[1].text
                    院校隶属 = i.select('td')[2].text
                    研究生院 = 1 if i.select('td')[3].select_one('i') else 0
                    自主划线 = 1 if i.select('td')[4].select_one('i') else 0
                    院校代码 = get_url_param(i.select('td')[5].select_one('a').attrs['href'])['dwdm']
                    院校1 = edu(院校名称=院校名称, 所在地=所在地, 院校隶属=院校隶属, 研究生院=研究生院,
                                自主划线=自主划线,
                                双一流=双一流, 院校代码=院校代码)
                    tmp_data.append(院校1.info())
                else:
                    self.store_in_database(tmp_data)

    def get_data(self):
        con = db_con().get_con()
        cur = con.cursor()
        cursor = cur.execute("SELECT *  FROM 院校库")
        data = [i for i in cursor]
        con.close()
        if len(data) == 0:
            self.__req_data()
            return self.get_data()
        else:
            return data

    @staticmethod
    def store_in_database(data):
        try:
            con = db_con.get_con()
            cur = con.cursor()
            cur.executemany(
                'INSERT INTO 院校库 (院校名称, 所在地, 院校隶属, 研究生院, 自划线院校, 院校代码, IS211, IS985, AB, 双一流)values (?,?,?,?,?,?,?,?,?,?) ',
                data)
            con.commit()
            con.close()
        except Exception:
            print(Exception)

# cur.execute('DELETE FROM 院校库')
# use2 = getEdu()
# use2.get_data()
