class yzw_table:

    @staticmethod
    def get_max_page(soup):
        '''
        此方法当前仅当页面处于第一页时有效
        :param soup:
        :return: 最大页码
        '''

        lip_list = soup.select('.ch-page .lip')
        for i in range(len(lip_list)):
            if 'dot' in lip_list[i].get('class'):
                k = i + 1
                break
        else:
            k = len(lip_list) - 2
        max_page_str = lip_list[k].select_one('a').text

        return int(max_page_str)

    @staticmethod
    def get_now_page(soup):

        now_page = soup.select_one('.lip.selected a').text
        return int(now_page)


