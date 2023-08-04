import os
import time

from yzw_dl.tools import output_jsonfile


def create_file_name(dlparams, session):
    name_mllb = session['mldm'][dlparams['mllb']]
    name_xklb = session['xklb'][dlparams['xklb']]
    name_xxfs = '全日制' if dlparams['xxfs'] == '1' else '非全日制'
    name_yxdq = f"{dlparams['yxdq']}区" if dlparams['yxdq'] in ['a', 'b'] else ''  # 院校地区
    name_yxjh = ''  # 院校计划
    name_zymc = dlparams['zymc']  # 专业名称
    # 将这些名字连接起来，但最多出现一个 - 作为分隔符
    name_list = [name_mllb, name_xklb, name_xxfs, name_yxdq, name_yxjh, name_zymc]
    name_list = [i for i in name_list if i != '']
    # 加个 20230515-12:00 这样的时间戳
    name_list.append(time.strftime("%Y%m%d-%H%M", time.localtime()))
    return '-'.join(name_list)


def save_jsonfile(data, save_name):
    # 保存数据
    out_file_path = os.path.join('static/dldocs', f'{save_name}.json')
    output_jsonfile(data, out_file_path)


def dlparams_to_id(dlparams, session):
    """
    将 dlparams 转换为 id
    """
    # 将字典的可以连接起来转换为字符串
    id = ''
    session['xklb']
    session['mldm']

    return '-'.join([str(i) for i in dlparams.values()])
