import requests
from bs4 import BeautifulSoup

from con_db import cur, con

cursor = cur.execute("SELECT url  FROM tmpzhaoshengdanwei")

data = [i[-1] for i in cursor]
yx_data = []
for i in data:

    while True:
        url = 'https://yz.chsi.com.cn/' + i
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text)

        for k in soup.select('.zsml-list-box tbody tr'):
            ksfs = k.select('td')[0].text
            yxs = k.select('td')[1].text
            zy = k.select('td')[2].text
            yjfx = k.select('td')[3].text
            xxfs = k.select('td')[4].text
            zdls = k.select('td')[5].text
            zsrs = k.select('td')[6].select_one('script').text
            ksfw = k.select('td')[7].select_one('a').get('href')
            bz = k.select('td')[8].text
            lrd = (i, ksfs, yxs, zy, yjfx, xxfs, zdls, zsrs, ksfw, bz)
            print(lrd[1:-1])
            yx_data.append(lrd)

        if 'unable' in soup.select_one('.lip-last').get('class'):
            break
        else:
            print(url)
            print('存在下一页')
            break

cur.execute('DELETE FROM tmpyuanxiaozhuanye ')
cur.executemany('INSERT INTO tmpyuanxiaozhuanye (yxlj, ksfs, yxs, zy, yjfx, xxfs, zdls, zsrs, ksfw, bz) VALUES (?,?,'
                '?,?,?,?,?,?,?,?)', yx_data)

con.commit()
con.close()
