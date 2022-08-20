import requests
from bs4 import BeautifulSoup

from db import con

r = con.execute('SELECT ksfw FROM recruit_major')

url = 'https://yz.chsi.com.cn'

for i in [i[-1] for i in r]:
    res = requests.get(url + i)
    soup = BeautifulSoup(res.text)

    zsdw = soup.select('.zsml-condition tbody tr .zsml-summary')

    zsde = soup.select('.zsml-result tbody tr td')
    print([i.text for i in zsdw] + [i.text for i in zsde])
