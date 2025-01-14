from enum import Enum
""" 請假類型 """
class LeaveType(Enum):
    PERSONAL = ("B", "事假")
    SICK = ("C", "病假")
    MATERNITY = ("H", "產假")
    OFFICIAL = ("A", "公假")
    MILITARY = ("S", "公假(兵役相關)")
    FUNERAL = ("F", "喪假")
    MARRIAGE = ("M", "婚假")
    MENTAL_HEALTH = ("N", "心理健康假")
    # EPIDEMIC = ("L", "防疫假")
    # VACCINATION = ("V", "疫苗接種假")
    PHYSIOLOGICAL = ("P", "生理假")

    def __init__(self, code, description):
        self.code = code
        self.description = description

""" 重要集會請假類別 """
class MeetingType(Enum):
    # 校慶＆運動會
    SCHOOL_CELEBRATION_AND_SPORTS_DAY = ("V001", "校慶＆運動會")
    # 運動會
    SPORTS_DAY = ("V002", "運動會")
    # 週會
    WEEKLY_MEETING = ("V003", "週會")
    # 其他集會
    OTHER_MEETINGS = ("V004", "其他集會")

    def __init__(self, code, description):
        self.code = code
        self.description = description