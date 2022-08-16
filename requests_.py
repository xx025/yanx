import requests


def req_method(url, data={}, method='post', params={}):
    print('打开：' + url)

    if method == 'post':
        if data is {}:
            page = requests.post(url)
        else:
            page = requests.post(url=url, data=data)
    elif method == 'get':
        if params == {}:
            page = requests.get(url=url)
        else:
            page = requests.get(url=url, params=params)

    print('加载成功')
    return page.text
