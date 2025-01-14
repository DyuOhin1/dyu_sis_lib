from enum import Enum

class LeaveResult(Enum):
    """
    將請假狀態對應到具體的消息，包括成功、失敗和錯誤等狀態。
    """
    
    SUCCESS = (
        "success", "請假完成。\r\n學生線上系統請假請記得隨時注意假單審核狀況。\r\n如假單未審核，請記得提醒老師。"
    )
    FAIL = (
        "fail", "請假失敗！\r\n可能原因有：\r\n1.證明文件的檔案大小超過2M(解決辦法：將證明文件縮減至2M以下)\r\n2.閒置過久(解決辦法：請重新登入)。"
    )
    BUSY = (
        "fail2", "請假失敗，系統繁忙中請稍後再試。"
    )

    PART_OF_UPLOAD = (
        "error_msg",
        "上傳檔案錯誤！\r\n原因：檔案僅被部分上傳。",
        3
    )

    FILE_NOT_UPLOAD = (
        "error_msg",
        "上傳檔案錯誤！\r\n原因：檔案未被上傳。",
        4
    )

    OVERSIZE_FILE = (
        "error_msg",
        "上傳檔案錯誤！\r\n原因：檔案未被上傳。",
        0
    )

    def __init__(self, key, message, msg_code=None):
        """
        初始化 LeaveResult
        :param key: function name
        :param message: function alert message
        :param msg_code: function parameter
        """

        self.key = key
        self.message = message

    @staticmethod
    def from_key(key, msg_code=None):
        """
        依照 key 和 msg_code 來取得 LeaveResult
        :param key: function name
        :param msg_code: function parameter
        :return:
        """

        # 如果 key 是 error_msg，則根據 msg_code 來判斷是哪種錯誤
        if key == "error_msg":
            # 如果 msg_code 不是 3 或 4，則代表檔案大小超過 2M
            if msg_code != 3 and msg_code != 4:
                return LeaveResult.OVERSIZE_FILE
            # 如果 msg_code 是 3，則代表檔案僅被部分上傳
            else:
                return LeaveResult.PART_OF_UPLOAD if msg_code == 3 else LeaveResult.FILE_NOT_UPLOAD

        # 依照 key 來取得 LeaveResult
        for result in LeaveResult:
            if result.key == key:
                return result

        return None