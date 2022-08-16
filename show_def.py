from selectable_params import location_code, xkml_code, xkly_code, zy_name


def show_welcome():
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


def show_codes(data: list):
    r_dict = dict()
    for i in range(data.__len__()):
        r_dict[data[i][0]] = data[i][1]
        if i != 0 and i % 5 == 0:
            print('\n', end='')
        print(data[i][1] + ':' + data[i][0] + '\t', end='')
    else:
        print('\n', end='')

    return r_dict


def xuanzediqu():
    print('1. 选择地区')
    data = location_code()
    sel_d = show_codes(data.get_data())

    re = input('请根据上面的地区选择一个地区，输入后面地区代码（如北京市：11）,如不选择地区输入 00 :')
    if re in sel_d:
        print('你选择的地区：' + re + sel_d[re])
    else:
        re = ''
        if re == '00':
            print('不选择地区')
        else:
            print('输入的地区代码不存在，已默认不做选择')
    return re


def xuanzemenlei():
    print('2. 选择门类')
    data = xkml_code()
    print('学术学位（学硕）：')
    d = show_codes(data.get_data())
    print('专业学位（专硕）：')
    print('专业学位：zyxw')
    re = input('请根据上面的学科选择一个学科，输入学科后面的代码（如 哲学:01）,*必选：')
    while True:
        if re in d:
            print('你的选择：学术学位' + re + d[re])
            break
        elif re == 'zyxw':
            print('你的选择：zyxw 专业学位')
            break
        else:
            print('选择错误')
            re = input('重新选择')
    return re


def xuanzelingyu(mldm='zyxw'):
    print('3.选择领域')
    m = xkly_code(dm=mldm)
    d = show_codes(m.get_data())
    re = input('请根据上面的学科领域选择一个学，输入学科领域后面的代码（如 哲学:0101）,*必选：')
    while True:
        if re in d:
            print('你的选择：' + re + d[re])
            break
        else:
            print('选择错误')
            re = input('重新选择')
    return re


def xuanzezhuanye(ly_code='0812'):
    print('4. 选择专业')
    zy = zy_name(ly_code=ly_code)
    zy_data = zy.get_data()
    the_in = input('你选择的领域共有' + str(len(zy_data)) + '个专业，是否选择具体专业？（是输入:y,否输入:n）:')
    if the_in == 'y':
        zy = show_codes(zy_data)
        re = input('请输入专业后面的代码：')
        while True:
            if re in zy:
                print('你的选择：' + re + zy[re])
                break
            else:
                print('选择错误')
                re = input('重新选择：')
    else:
        pass


def xuenzexuexifangshi():
    print('5. 学习方式')
    xxfs = input('全日制：1 ,非全日制：2 ，不做选择：0 :')
    if xxfs == 1 or xxfs == 2:
        pass
    else:
        xxfs = ''
    return xxfs
