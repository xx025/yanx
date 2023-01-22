import re

from bs4 import BeautifulSoup

from stools.sk3 import req_get


def get_year():
    try:
        url = 'https://yz.chsi.com.cn/zsml/zyfx_search.jsp'

        text = req_get(url=url).text
        soup = BeautifulSoup(text, 'html.parser')
        lt = soup.select_one('.zsml-form-box h2').text
        lt = re.findall("\d+", lt)[0]
        lt = int(lt)
    except:
        lt = None
    return lt
