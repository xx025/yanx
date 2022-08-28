from dl_s.get_major_details import dl_details
from dl_s.get_recruit_majors import dl_majors
from dl_s.get_recruit_schools import dl_schools


@staticmethod
class dlYzw:
    def __init__(self):
        self.dl_majors = dl_majors()
        self.dl_schools = dl_schools()
        self.dl_details = dl_details()
