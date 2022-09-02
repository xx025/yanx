from download_university_info.get_major_details import dl_details
from download_university_info.get_recruit_majors import dl_majors
from download_university_info.get_recruit_schools import dl_schools


class dlYzw:
    def __init__(self):
        self.dl_schools = dl_schools()
        self.dl_majors = dl_majors()
        self.dl_details = dl_details()
