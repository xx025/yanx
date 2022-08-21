from dl_s.get_recruit_majors import dl_majors
from dl_s.get_recruit_schools import dl_schools


@staticmethod
class dl_yzw:
    def __init__(self):
        self.dl_majors = dl_majors()
        self.dl_schools = dl_schools()
