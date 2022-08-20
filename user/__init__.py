from user.selectable_params import xkml_code, xkly_code, zy_name, location_code, choice

from user.yzw_pages import dl_yzw


class user:
    def __init__(self):
        self.__location_codes = None
        self.__discipline_code = ''
        self.__field_of_study_code = ''
        self.__majors = None
        self.__learn_mode = None
        self.choice = choice()
        self.__construction_plans = {'211': '0', '985': '0', '11': '0'}
        self.dl_yzw = dl_yzw()

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

    def set_discipline(self):
        pass

    def set_field_of_study(self):
        pass

    def set_major(self):
        pass

    def set_learn_way(self):
        pass

    def set_location(self):
        pass

    def set_construction_plans(self):
        self.choice.set_hh()

    def __set_dl_school(self):
        self.dl_yzw.dl_schools.set_user_select_datas(self.get_user_choice_items())

    def dl_schools(self):
        self.__set_dl_school()
        self.dl_yzw.dl_schools.dl_data()

    def __set_dl_major(self):
        self.dl_yzw.dl_majors.set_rules(self.__construction_plans)

    def dl_majors(self):
        self.__set_dl_major()
        self.dl_yzw.dl_majors.dl_data()
