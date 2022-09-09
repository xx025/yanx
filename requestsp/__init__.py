from time import sleep

import requests

from global_values import global_queue


def get(url: str, param=None):
    i = 1
    while True:

        try:
            if param is None:
                return requests.get(url=url, timeout=6)
            else:
                return requests.get(url=url, params=param, timeout=6)
        except Exception:
            k = 2 ** i
            global_queue.put("第{}次，请求失败，等待{}s 后继续".format(i, k))
            sleep(k)
            i += 1
            if i > 9:
                break


def post(url: str, data=None):
    i = 1
    while True:
        try:
            if data is None:
                return requests.post(url=url, timeout=6)
            else:
                return requests.post(url=url, data=data, timeout=6)
        except Exception:
            k = 2 ** i
            global_queue.put("第{}次，请求失败，等待{}s 后继续".format(i, k))
            sleep(k)
            i += 1
            if i > 9:
                break
