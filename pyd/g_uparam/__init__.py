def get_url_param(url: str):
    from urllib.parse import urlparse, parse_qs
    query = urlparse(url).query
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])
