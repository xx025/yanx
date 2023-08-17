from yzw_dl.DownTask import DownTask
from yzw_dl.tools import parse_config


class YanxDownTask(DownTask):

    def __init__(self, dlparams, save_json_path):
        self.dl_params = dlparams
        self.param_list = parse_config(self.tarnsform_dlparams())
        super().__init__(param_list=self.param_list, save_json_file=[True, save_json_path], save_csv_file=[False, 1, 1])

    def tarnsform_dlparams(self):
        # 和yzw_dl中的参数对齐
        dl_params = self.dl_params
        config_values = {'ssdm': '',
                         'dwmc': '',
                         'mldm': dl_params.get('mllb', ''),
                         'yjxkdm': dl_params.get('xklb', ''),
                         'zymc': dl_params.get('zymc', ''),
                         'xxfs': dl_params.get('xxfs', '')
                         }
        return config_values
