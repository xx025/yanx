from db import con, cur
from deal_text.print_txt import print_t
from dl_s import dlYzw
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
        self.dl_yzw = dlYzw()

        self.con = con
        self.cur = cur

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

    def __set_dl_school(self):
        self.dl_yzw.dl_schools.set_user_select_datas(self.get_user_choice_items())

    def __set_dl_major(self):
        self.dl_yzw.dl_majors.set_rules(self.__construction_plans, con=self.con, cur=self.cur)

    def dl_schools(self):
        self.__set_dl_school()
        self.dl_yzw.dl_schools.dl_data(con=self.con, cur=self.cur)

    def dl_majors(self):
        self.__set_dl_major()
        self.dl_yzw.dl_majors.dl_data(con=self.con, cur=self.cur)

    def dl_details(self):
        self.dl_yzw.dl_details.dl_data(con=self.con, cur=self.cur)

    def dl_all(self):
        self.dl_schools()
        self.dl_majors()
        self.dl_details()

        GLOBALS_DICT['down_end'] = True

        print_t("全部下载结束")
