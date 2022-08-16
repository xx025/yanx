import requests


def req_post(url, data={}):
    print('打开：' + url)

    if data is {}:
        page = requests.post(url)
    else:
        page = requests.post(url=url, data=data)

    print('加载成功')
    return page.text
