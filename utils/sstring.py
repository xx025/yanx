def remove_spaces(strs=''):
    return strs.replace('\n', '').replace('\r', '').replace(' ', '')


def get_url_param(url: str):
    from urllib.parse import urlparse, parse_qs
    query = urlparse(url).query
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])
