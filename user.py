from selectable_params import location_code, xkml_code, xkly_code, zy_name
from show_def import show_codes


class user:
    def __init__(self):
        self.locations = []
        self.me_lei = ''

    def xuanzediqu(self):
        print('1. 选择地区')

        ab = input('是否选择区分A区或B区?(A区：a ,B区：b ，不做区分按回车键 ):')

        data = location_code()
        locs = data.get_data(ab)

        sel_d = show_codes(locs)

        input_str = input(
            '请根据上面的地区选择一个地区，输入后面地区代码（如北京市：11）,选择多个请用空格隔开,选择全部敲回车键 :').strip()

        if input_str == '':
            self.locations = [k[0] for k in locs]
        else:
            tmp_locations = input_str.split(' ')
            for i in tmp_locations:
                if i in sel_d:
                    self.locations.append(i)

        k = 0
        for i in self.locations:
            print(' ' * 3 + i + ':' + sel_d[i], end='')
            k += 1
            if k % 5 == 0:
                print()
        else:
            print()
        return self.locations

    def xuanzemenlei(self):
        print('2. 选择门类')
        data = xkml_code()
        print('学术学位（学硕）：')
        d = show_codes(data.get_data())
        print('专业学位（专硕）：')
        print(' ' * 3 + '专业学位：zyxw')
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

    def xuanzelingyu(self, mldm='zyxw'):
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

    def xuanzezhuanye(self, ly_code='0812'):
        print('4. 选择专业')
        zy = zy_name(ly_code=ly_code)
        zy_data = zy.get_data()
        the_in = input('你选择的领域共有' + str(len(zy_data)) + '个专业，是否选择具体专业？（是输入:y,否输入:n）:')
        if the_in == 'y':
            zy = show_codes(zy_data)
            re = input('请输入专业后面的代码，选择多个请用空格隔开：')
            while True:
                if re in zy:
                    print('你的选择：' + re + zy[re])
                    break
                else:
                    print('选择错误')
                    re = input('重新选择：')
        else:
            pass

    def xuenzexuexifangshi(self):
        print('5. 学习方式')
        xxfs = input('全日制：1 ,非全日制：2 ，不做选择回车 :')
        if xxfs == 1 or xxfs == 2:
            pass
        else:
            xxfs = ''
        return xxfs
