from enum import Enum


class Lang(Enum):
    ZH_TW = "zh-TW"
    ZH_CN = "zh-CN"
    EN = "en"

    def __init__(self, code):
        self.code = code