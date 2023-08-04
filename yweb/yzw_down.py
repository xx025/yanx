import os
import threading
import time

from yzw_dl import dl_zsyx, dl_yxzy, dl_ksfw
from yzw_dl.tools import parse_config, output_jsonfile


class DownTask(threading.Thread):

    def __init__(self, dlparams, save_name):
        super().__init__()
        self.dlparams = dlparams
        self.config_values = self.tarnsform_dlparams()
        self.dl_progress = {
            '院校信息': 0,
            '专业信息': 0,
            '考试信息': 0
        }
        self.save_name = save_name
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

    def tarnsform_dlparams(self):
        # 和yzw_dl中的函数的对其

        dlparams = self.dlparams
        config_values = {}
        config_values['ssdm'] = ''  # 省市代码
        config_values['dwmc'] = ''  # 单位名称
        config_values['mldm'] = dlparams.get('mllb', '')  # 门类类别
        config_values['yjxkdm'] = dlparams.get('xklb', '')  # 学科类别
        config_values['zymc'] = dlparams.get('zymc', '')  # 专业名称
        config_values['xxfs'] = dlparams.get('xxfs', '')  # 学习方式
        return config_values

    def get_dl_progress(self):
        return self.dl_progress

    def stop(self):
        self._stop_event.set()

    def run(self):
        config_values = self.config_values  # 下载参数
        progress_data = self.dl_progress  # 进度信息
        param_list = parse_config(config_values)  # 解析后的参数列表
        Dl_Data = {}
        # 构造进度信息的初始状态
        for i_ in range(len(param_list)):
            _param = param_list[i_]
            progress_data["院校信息"] = int((i_ + 1) / len(param_list) * 100)
            for sch in dl_zsyx(**_param):
                Dl_Data[sch.招生单位] = sch.dict()
        # 院校信息下载完成后，开始下载专业信息
        Dl_Data_keys = list(Dl_Data.keys())
        for j_ in range(len(Dl_Data_keys)):
            progress_data["专业信息"] = int((j_ + 1) / len(Dl_Data_keys) * 100)
            key = Dl_Data_keys[j_]
            param = Dl_Data[key]['dl_params']
            Dl_Data[key]['招生专业'] = {zs.id: zs.dict() for zs in dl_yxzy(**param)}
        for k_ in range(len(Dl_Data_keys)):
            key = Dl_Data_keys[k_]
            progress_data["考试信息"] = int((k_ + 1) / len(Dl_Data_keys) * 100)
            for zyid in Dl_Data[key]['招生专业'].keys():
                my_dl_ksfw = dl_ksfw(zyid)
                zsml = my_dl_ksfw['zsml'].dict()  # 在详情页面会有一些更详细的信息
                ksfw = [ks_.dict() for ks_ in my_dl_ksfw['ksfw']]  # 考试科目范围
                dict1 = Dl_Data[key]['招生专业'][zyid]
                dict1.update(zsml)  # 更新招生专业信息
                dict1['考试范围'] = ksfw  # 添加考试科目范围
                Dl_Data[key]['招生专业'][zyid] = dict1  # 更新招生专业信息

        # 保存数据
        output_jsonfile(Dl_Data, os.path.join('dldocs', f'{self.save_name}.json'))

        progress_data = {key: 100 for key in progress_data.keys()}
        # 发送初始进度信息给前端
        _ = progress_data

        while True:
            if self._stop_event.is_set():
                break
            time.sleep(1)

    # 保存数据
