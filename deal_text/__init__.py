from urllib.parse import urlparse, parse_qs


def replace_bank(strs=''):
    return strs.replace('\n', '').replace('\r', '').replace(' ', '')


def get_url_param(url: str):
    query = urlparse(url).query
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])


