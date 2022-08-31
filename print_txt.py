GLOBALS_DICT = {'text_area': None}


def print_t(text):
    try:
        GLOBALS_DICT['text_area'].append(text)
        GLOBALS_DICT['text_area'].moveCursor(GLOBALS_DICT['text_area'].textCursor().End)  # 文本框显示到底部
    except Exception as e:
        print(e)
