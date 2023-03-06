from time import sleep

import requests

from _g.g3 import global_queue


def req_post(url: str, data=None):
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
                global_queue.put("下载不动啦，请重新运行程序")
                break


def req_get(url: str, params=None):
    i = 1
    while True:

        try:
            if params is None:
                return requests.get(url=url, timeout=6)
            else:
                return requests.get(url=url, params=params, timeout=6)
        except Exception:
            k = 2 ** i
            global_queue.put("第{}次，请求失败，等待{}s 后继续".format(i, k))
            sleep(k)
            i += 1
            if i > 9:
                global_queue.put("下载不动啦，请重新运行程序")
                break
