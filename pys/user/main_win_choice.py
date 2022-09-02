from pys.download_university_info.selectable_params import location_code


class choice:

    @staticmethod
    def c_constraction_plans(select_str: str):
        code = {'211': '0', '985': '0', '11': '0'}
        if select_str == '双一流':
            code['11'] = 1
        elif select_str == '985':
            code['985'] = 1
        elif select_str == '211':
            code['211'] = 1
        else:
            pass
        return code

    @staticmethod
    def c_location(location: str):
        if location == '不做选择':
            location = None
        else:
            if location == 'A区':
                location = 'a'
            else:
                location = 'b'
            data = location_code()
            location = data.get_data(ab=location)
            location = [i[0] for i in location]
        return location

    @staticmethod
    def c_discipline(*discipline: str):
        if discipline[0] == '专业学位':
            code = 'zyxw'
        else:
            code = discipline[1].split(' ')[0]
        return code

    @staticmethod
    def c_field_of_study(filed_code: str):

        return filed_code.split(' ')[0]

    @staticmethod
    def c_learn_mode(learn_mode_s: str):
        if learn_mode_s == '全日制':
            return 1
        elif learn_mode_s == '非全日制':
            return 2
        else:
            return None
