#!/usr/bin/python3
# coding:  utf8
# @File    : count.py
# @author  :xx025
import json
from eduList import list211 ,list985


for i in list985:
    if i not in list211:
        print(i)
else:
    print('list985 包含于 list211')

print("211:{}所 \t 985:{}所".format(len(list211),len(list985)))
rList985 = []
rList211 = []

with open('documentation/edudata.json', encoding='utf8') as f:
    data = json.load(f)
for i in data['data']:
    if ('985' in i['计划']):
        rList985.append(i['院校名称'])
    if (i['计划'] == '211'):
        rList211.append(i['院校名称'])

print("211:{} 所 \t985:{}所 共：{} 所".format(len(rList211),len(rList985),len(rList985)+len(rList211)))

for i in list985:
    if i not in rList985:
        print(i)

print("--------------")
for i in list211:
    if i not in rList211 and i not in list985:
        print(i)
