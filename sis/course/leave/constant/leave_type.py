from enum import Enum

""" 請假類型 """
class LeaveType(str, Enum):
    PERSONAL = "B"  # 事假
    SICK = "C"  # 病假
    MATERNITY = "H"  # 產假
    OFFICIAL = "A"  # 公假
    MILITARY = "S"  # 公假(兵役相關)
    FUNERAL = "F"  # 喪假
    MARRIAGE = "M"  # 婚假
    MENTAL_HEALTH = "N"  # 心理健康假
    PHYSIOLOGICAL = "P"  # 生理假

    @property
    def description(self):
        descriptions = {
            "B": "事假",
            "C": "病假",
            "H": "產假",
            "A": "公假",
            "S": "公假(兵役相關)",
            "F": "喪假",
            "M": "婚假",
            "N": "心理健康假",
            "P": "生理假"
        }
        return descriptions[self.value]

""" 重要集會請假類別 """
class MeetingType(str, Enum):
    SCHOOL_CELEBRATION_AND_SPORTS_DAY = "V001"  # 校慶＆運動會
    SPORTS_DAY = "V002"  # 運動會
    WEEKLY_MEETING = "V003"  # 週會
    OTHER_MEETINGS = "V004"  # 其他集會

    @property
    def description(self):
        descriptions = {
            "V001": "校慶＆運動會",
            "V002": "運動會",
            "V003": "週會",
            "V004": "其他集會"
        }
        return descriptions[self.value]
