sql_yxk = '''create table main.院校库
(
    院校名称   TEXT not null,
    所在地     TEXT not null,
    院校隶属   TEXT,
    研究生院   TEXT,
    自划线院校 TEXT,
    院校代码   TEXT not null
        constraint 院校库_pk
            primary key,
    IS211      TEXT,
    IS985      TEXT,
    AB         TEXT,
    双一流     TEXT,
    博士点     text
);
'''

sql_table_ksfw = '''create table main.考试范围
(
    id               TEXT not null,
    tid              TEXT,
    political        TEXT not null,
    foreign_language TEXT not null,
    pro_course_1     TEXT not null,
    pro_course_2     TEXT not null
);'''

sql_table_zszy = '''
create table main.招生专业
(
    id                 TEXT not null,
    tid                TEXT,
    enrollment_unit    TEXT,
    examination_method TEXT,
    departments        TEXT,
    major              TEXT,
    learning_style     TEXT,
    research_direction TEXT,
    instructor         TEXT,
    number_recruit     TEXT
);
'''

sql_table_xzre = '''
create table main.下载任务
(
    dname     text,
    id        text
        primary key,
    available TEXT,
    atime     text
);
'''

sql_table_dydm = '''
create table main.地区代码
(
    dm text
        constraint table_name_pk
            primary key,
    mc text,
    ab text
);
'''

sql_table_dqdm = '''insert into 地区代码 (dm, mc, ab)
values  ('11', '北京市', 'a'),
        ('12', '天津市', 'a'),
        ('13', '河北省', 'a'),
        ('14', '山西省', 'a'),
        ('15', '内蒙古自治区', 'b'),
        ('21', '辽宁省', 'a'),
        ('22', '吉林省', 'a'),
        ('23', '黑龙江省', 'a'),
        ('31', '上海市', 'a'),
        ('32', '江苏省', 'a'),
        ('33', '浙江省', 'a'),
        ('34', '安徽省', 'a'),
        ('35', '福建省', 'a'),
        ('36', '江西省', 'a'),
        ('37', '山东省', 'a'),
        ('41', '河南省', 'a'),
        ('42', '湖北省', 'a'),
        ('43', '湖南省', 'a'),
        ('44', '广东省', 'a'),
        ('45', '广西壮族自治区', 'b'),
        ('46', '海南省', 'b'),
        ('50', '重庆市', 'a'),
        ('51', '四川省', 'a'),
        ('52', '贵州省', 'b'),
        ('53', '云南省', 'b'),
        ('54', '西藏自治区', 'b'),
        ('61', '陕西省', 'a'),
        ('62', '甘肃省', 'b'),
        ('63', '青海省', 'b'),
        ('64', '宁夏回族自治区', 'b'),
        ('65', '新疆维吾尔自治区', 'b');
        '''

sqls = {'地区代码': sql_table_dydm,
        '下载任务': sql_table_xzre,
        '招生专业': sql_table_zszy,
        '考试范围': sql_table_ksfw,
        '院校库': sql_yxk}
