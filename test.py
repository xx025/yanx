import json

import requests

r = requests.post(url='https://yz.chsi.com.cn/zsml/code/zy.do', data={'q': '0782'})


print(r.text)
