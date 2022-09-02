from urllib.parse import urlparse, parse_qs


def replace_bank(strs=''):
    return strs.replace('\n', '').replace('\r', '').replace(' ', '')


def get_url_param(url: str):
    query = urlparse(url).query
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])


from pys.global_values import GLOBALS_DICT
import logging


Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename="logfile.log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.ERROR)

logger = logging.getLogger()
logger.error("Our First Log Message")


def print_t(t):
    try:
        if type(t) != str:
            logger.log(msg=t, level=0)
        else:
            GLOBALS_DICT['text_area'].append(t)
            GLOBALS_DICT['text_area'].moveCursor(GLOBALS_DICT['text_area'].textCursor().End)  # 文本框显示到底部

    except Exception as e:
        print_t(e)
