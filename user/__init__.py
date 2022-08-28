from dl_s import dlYzw
from user.selectable_params import xkml_code, xkly_code, zy_name, location_code, choice


class user:
    def __init__(self):
        self.__discipline_code = ''
        self.__field_of_study_code = ''
        self.__majors = None

        self.__location_codes = None
        self.__learn_mode = None
        self.__construction_plans = None

        self.choice = choice()
        self.dl_yzw = dlYzw()

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
        self.__discipline_code = self.choice.discipline()

    def set_field_of_study(self):
        self.__field_of_study_code = self.choice.field_of_study(dm=self.__discipline_code)

    def set_major(self):
        self.__majors = self.choice.major(self.__field_of_study_code)

    def set_learn_way(self):
        self.__learn_mode = self.choice.learn_code()

    def set_location(self):
        self.__location_codes = self.choice.location()

    def set_construction_plans(self):
        self.__construction_plans = self.choice.construction_plan()

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

    def dl_details(self):
        self.dl_yzw.dl_details.dl_data()
