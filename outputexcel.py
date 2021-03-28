#!/usr/bin/python3
# coding:  utf8
# @File    : outputexcel.py.py
# @author  :xx025

'''
此脚本是为了将json数据输出到表格
'''
import json

with open('documentation/edudata.json', encoding='utf8') as f:
    data = json.load(f)
for i in data['data']:
    print(i)

import xlwings as xw

info = list()
for i in data['data']:
    info.append([k for j, k in i.items()])

wb = xw.Book()

sht = wb.sheets['Sheet1']
sht.range('A1').value = '院校库'
sht.range('A2:I2').value = ['计划', 'AB区', '院校名称', '所在地', '院校隶属', '研究生院', '自划线院校',
                            '网报公告', '招生简章', '在线咨询', '调剂办法']

sht.range('A3').options(expand='table').value = info
sht.range('a1:k1').api.merge()  # 合并

wb.save('documentation/院校库.xlsx')
