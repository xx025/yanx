import time

from global_values import global_vals


def create_file_name(dlparams):
    name_mllb = global_vals['mllb'][dlparams['mllb']]
    name_xklb = global_vals['xklb'][dlparams['xklb']]
    name_xxfs = '全日制' if dlparams['xxfs'] == '1' else '非全日制'
    name_yxdq = f"{dlparams['yxdq']}区" if dlparams['yxdq'] in ['a', 'b'] else ''  # 院校地区
    name_yxjh = ''  # 院校计划
    name_zymc = dlparams['zymc']  # 专业名称
    # 将这些名字连接起来，但最多出现一个 - 作为分隔符
    name_list = [name_mllb, name_xklb, name_xxfs, name_yxdq, name_yxjh, name_zymc]
    name_list = [i for i in name_list if i != '']
    # 加个 20230515 这样的时间戳
    name_list.append(time.strftime("%Y%m%d", time.localtime()))
    return '-'.join(name_list)


