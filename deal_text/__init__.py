def replace_bank(strs=''):
    return strs.replace('\n', '').replace('\r', '').replace(' ', '')


def get_url_param(url: str):
    '''

    :param url:
    :return:
    '''
    ts = replace_bank(url)
    param = {}
    for i in ts.split('?')[-1].split('&'):
        (key, val) = tuple(i.split('='))
        param[key] = val
    return param
