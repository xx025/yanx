#!/usr/bin/python3
# coding:  utf8
# @File    : yxk.py.py
# @author  :xx025

'''
此脚本是为了将院校库json数据输出到表格
'''
import json
from time import sleep

with open('../uinnfo/edudata.json', encoding='utf8') as f:
    data = json.load(f)

import xlwings as xw

info = list()
infoUrl=[]
for i in data['data']:
    info.append([k for j, k in i.items()][:7])
    infoUrl.append([k for j, k in i.items()][7:])



wb = xw.Book()

sht = wb.sheets['Sheet1']
sht.range('A1').value = '院校库'
sht.range('a1:k1').api.merge()  # 合并
sht.range('A2:I2').value = ['计划', 'AB区', '院校名称', '所在地', '院校隶属', '研究生院', '自划线院校',
                            '网报公告', '招生简章', '在线咨询', '调剂办法']

sht.range('A3').options(expand='table').value = info

# h3-k3
# ?   ?
#

kliy=['网报公告', '招生简章', '在线咨询', '调剂办法']
max_col=len(infoUrl)

for i in range(max_col):
    try:
        u=infoUrl[i]
        ldh = 'H' + str(i + 3)
        ldI = 'I' + str(i + 3)
        ldJ = 'J' + str(i + 3)
        ldK = 'K' + str(i + 3)
        sht.range(ldh).add_hyperlink(u[0], text_to_display=kliy[0], screen_tip=None)
        sht.range(ldJ).add_hyperlink(u[1], text_to_display=kliy[1], screen_tip=None)
        sht.range(ldI).add_hyperlink(u[2], text_to_display=kliy[2], screen_tip=None)
        sht.range(ldK).add_hyperlink(u[3], text_to_display=kliy[3], screen_tip=None)
        sleep(0.03)
    except:
        pass

wb.save('../documentation/院校库.xlsx')
