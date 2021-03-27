#!/usr/bin/python3
# coding:  utf8
# @File    : count.py
# @author  :xx025
import json
from eduList import list211 ,list985


rList985 = []
rList211 = []

with open('edudata.json', encoding='utf8') as f:
    data = json.load(f)
for i in data['data']:
    if ('985' in i['计划']):
        rList985.append(i['院校名称'])
    if (i['计划'] == '211'):
        rList211.append(i['院校名称'])

print(len(rList985))
print(len(rList211))

print(len(rList985)+len(rList211))
for i in list985:
    if i not in rList985:
        print(i)

print("--------------")
for i in list211:
    if i not in rList211 and i not in list985:
        print(i)
