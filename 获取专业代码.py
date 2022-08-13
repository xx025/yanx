import json

import requests

from con_db import con, cur

# 获取学术或专业代码
r = requests.get('https://yz.chsi.com.cn/zsml/pages/getMl.jsp')

data = [(k['dm'], k['mc'], '学术学位') for k in json.loads(r.text)]

cur.executemany('INSERT INTO xuekemenlei (dm, mc,class) VALUES (?,?,? )', data)

cur.execute('INSERT INTO xuekemenlei (dm, mc,class) VALUES (?,? ,?)', ('zyxw', '专业学位', '专业学位'))

con.commit()

# 获取学科门类或领域

cursor = cur.execute("SELECT *  FROM xuekemenlei")

xue_ke_dai_ma = [i for i in cursor]

for i in xue_ke_dai_ma:
    print(i)

    xk_code = i[0]
    r = requests.post(url='https://yz.chsi.com.cn/zsml/pages/getZy.jsp', data={'mldm': xk_code})

    data = [(xk_code, k['mc'], k['dm']) for k in json.loads(r.text)]
    cur.executemany('INSERT INTO xuekemenleilingyu (xkml,mc,dm) VALUES (?,?,?)', data)

else:
    con.commit()
    print('完毕')

# 获取专业名字
cursor = cur.execute("SELECT dm  FROM xuekemenleilingyu")

# 全部专业代码
data = [i[0] for i in cursor]
for zy_code in data:
    r = requests.post(url='https://yz.chsi.com.cn/zsml/code/zy.do', data={'q': zy_code})
    try:
        data = [(zy_code, i) for i in json.loads(r.text)]
        print(data)
        cur.executemany('INSERT INTO allzhuanye (zy_code, name) VALUES (?,?)', data)
    except:
        pass

else:
    con.commit()
    con.close()
