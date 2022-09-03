from pys.download_university_info import dlYzw
from global_values import GLOBALS_DICT


class user:
    def __init__(self):
        self.__discipline_code = ''
        self.__field_of_study_code = ''
        self.__majors = None

        self.__location_codes = None
        self.__learn_mode = None
        self.__construction_plans = None

        # self.choice = choice()
        self.text_area = None
        self.dl_yzw = None


    def get_user_choice_items(self):
        """

        :return:
        'location_codes': self.__location_codes,
        'discipline': self.__discipline,
        'field_of_study': self.__field_of_study,
        'majors': self.__majors,
        'learn_mode': self.__learn_mode,
        'construction_plans': self.__construction_plans
        """
        return {'location_codes': self.__location_codes,
                'discipline_code': self.__discipline_code,
                'field_of_study_code': self.__field_of_study_code,
                'majors': self.__majors,
                'learn_mode': self.__learn_mode,
                'construction_plans': self.__construction_plans
                }

    def set_user_choice_items(self,
                              location_codes,
                              discipline_code,
                              field_of_study_code,
                              majors,
                              learn_mode,
                              construction_plans):
        self.__location_codes = location_codes
        self.__discipline_code = discipline_code
        self.__field_of_study_code = field_of_study_code
        self.__majors = majors
        self.__learn_mode = learn_mode
        self.__construction_plans = construction_plans

    def set_discipline(self, code):
        self.__discipline_code = code

    def set_field_of_study(self, code):
        self.__field_of_study_code = code

    def set_major(self):
        self.__majors = ""

    def set_learn_way(self, code):
        self.__learn_mode = code

    def set_location(self, loca_code):
        self.__location_codes = loca_code

    def set_construction_plans(self, code):
        self.__construction_plans = code

    def dl_all(self):
        self.dl_yzw = dlYzw(user_choice=self.get_user_choice_items())
        self.dl_yzw.down_all()
        GLOBALS_DICT['down_end'] = True

        print("全部下载结束")
