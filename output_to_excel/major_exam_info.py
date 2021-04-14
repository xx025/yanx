import json
import os.path

import xlwings as xw

with open('../uinnfo/link_loc_uni.json', encoding='utf8') as f:
    link_loc_uni = json.load(f)

# 读文件夹文件，获取文件名列表
u_list = []
for filename in os.listdir("../college_majors_exam_scope/zyxw/"):
    u_list.append('{}'.format(filename[:-5]))

# 读文件
udict = {}
allMagorsInfo = []
for filename in u_list:
    with open('../college_majors_exam_scope/zyxw/{}.json'.format(filename), 'r', encoding='utf8') as f:
        load_dict = json.load(f)
    udict[filename] = [u for u in load_dict[filename]]
    for k in load_dict[filename]:
        specificInfo = [filename] + link_loc_uni[filename] + [v for u, v in k.items()][:-1] + [nn for nn, mm in
                                                                                               k['考试科目'].items()]
        allMagorsInfo.append(specificInfo)


wb = xw.Book()

list2 = ['院校', '计划', 'AB区', '所在地'] + ["招生单位", "考试方式", "院系所", "跨专业", "专业", "学习方式", "研究方向", "指导老师", "拟招人数", "备注", "考试科目1", "考试科目2", "考试科目3",
                 "考试科目4"]
sht = wb.sheets['Sheet1']
sht.range('A1').value = '院校体招生专业、招生人数和考试科目等'
sht.range('a1:k1').api.merge()  # 合并
sht.range('A2:R2').value =list2
sht.range('A3').options(expand='table').value = allMagorsInfo
wb.save('../documentation/院校专业-专硕-0854.xlsx')
