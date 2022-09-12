from pyd.db import db_con


class dlYzw:

    def __init__(self, user_choice):
        from pyd.gdms.get_major_details import dl_details
        from pyd.gdms.get_recruit_majors import dl_majors
        from pyd.gdms.get_recruit_schools import dl_schools

        self.__con = db_con.get_con()
        # 获取数据库连接
        self.__schools = dl_schools(self.__con)
        self.__majors = dl_majors(self.__con)
        self.__details = dl_details(self.__con)
        self.__user_choice = user_choice

    def __dl_school(self):
        self.__schools.set_user_select_datas(self.__user_choice)
        self.__schools.dl_data()

    def __dl_majors(self):
        self.__majors.set_rules(self.__user_choice.get('construction_plans'))
        self.__majors.dl_data()

    def __dl_details(self):
        self.__details.dl_data()

    def down_all(self):
        self.__dl_school()
        self.__dl_majors()
        self.__dl_details()
        self.__con.close()
        # 关闭数据库连接
