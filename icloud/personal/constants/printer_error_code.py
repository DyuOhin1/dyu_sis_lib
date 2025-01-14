from enum import Enum


class PrinterErrorCode(Enum):
    TEST_MESSAGE = (2600, "測試訊息")
    SUCCESS = (1, "驗證成功​")
    ENGLISH_NAME_SAVED = (2, "英文姓名儲存成功")
    PRINT_POINTS_QUERY_SUCCESS = (3, "列印點數查詢成功")
    LEAVE_REVIEW_SUCCESS = (4, "差假審核成功")
    PROXY_SAVED = (5, "職務代理人儲存成功")
    TASK_SAVED = (6, "業務職掌儲存成功")
    LINK_PUBLISHED = (7, "發布連結成功！")
    LINK_ADDED = (8, "新增連結成功！")
    LINK_MODIFIED = (9, "修改連結成功！")
    LINK_DELETED = (10, "刪除連結成功！")
    REMOVED_FROM_GROUP = (11, "已從群組中移除！")
    SAVED_SUCCESSFULLY = (12, "儲存成功！")
    UNPINNED_SUCCESSFULLY = (13, "已取消置頂！")
    PIN_TOGGLE_SUCCESS = (14, "置頂切換成功！")
    LINK_REMOVED = (15, "已移除該連結！")
    PUBLISH_STATUS_CHANGED = (16, "發佈狀態更改成功！")
    LEAVE_PROCEDURE_STARTED = (17, "您的離校手續已啟動，請至「進度追踨」頁面!(5秒後自動切換)")
    IDLE_TIMEOUT = (-1, "您閒置過久，請重新登入!")
    SYSTEM_ERROR = (-2, "系統發生問題，如有問題請洽電算中心!")
    NO_PERMISSION = (-3, "您沒有使用權限，如有問題請洽電算中心!")
    ENGLISH_NAME_SAVE_FAILED = (-4, "英文姓名儲存失敗")
    DATA_TRANSMISSION_ERROR = (-5, "資料傳輸有誤，請洽電算中心")
    PRINT_POINTS_QUERY_FAILED = (-6, "列印點數查詢失敗")
    SELECT_PENDING_DATA = (-7, "請點選待審資料")
    REVIEW_DATA_ERROR = (-8, "送審資料有誤")
    LEAVE_REVIEW_FAILED = (-9, "差假審核失敗")
    PROXY_SAVE_FAILED = (-10, "職務代理人儲存失敗")
    TASK_SAVE_FAILED = (-11, "業務職掌儲存失敗")
    NO_OPERATION_PERMISSION = (-12, "您沒有操作權限！")
    COMPLETE_CHINESE_DESCRIPTION = (-13, "請完成中文描述欄位！")
    COMPLETE_URL_FIELD = (-14, "請完成網址欄位！")
    SELECT_START_END_TIME = (-15, "請選擇起迄時間！")
    SELECT_START_TIME = (-16, "請選擇開始時間！")
    SELECT_END_TIME = (-17, "請選擇結束時間！")
    UPLOAD_IMAGE = (-18, "請上傳圖片！")
    IMAGE_FORMAT_ERROR = (-19, "只允許上傳jpg、png或gif檔！")
    WRITE_FAILED = (-20, "寫入失敗！")
    NOT_GRADUATING = (-21, "您非應屆畢業生，不可啟動離校手續 !")
    LEAVE_ONLINE_PROCESS_NOT_ALLOWED = (-22, "您目前為休學或退學狀態，無法啟動線上離校手續，請改以紙本離校流程辦理!")
    CHECKPOINTS_NOT_COMPLETED = (-23, "您尚有部份關卡未通過，無法啟動 !")
    LEAVE_PROCEDURE_NOT_STARTED = (-24, "您的離校手續尚未啟動，請至「我要啟動」頁面 !(5秒後自動切換)")
    MENTOR_NOT_ASSIGNED = (-25, "您的師徒導師尚未設定，請洽系助理設定您本學期的「師徒導師」 !")
    ADVISOR_NOT_ASSIGNED = (-26, "您的指導教授尚未設定，請到學生資訊系統設定!")
    DEPT_ASSISTANT_ERROR = (-27, "讀取系助理關卡資料錯誤，請洽電算中心 !")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @staticmethod
    def get_description_by_code(code):
        for message in PrinterErrorCode:
            if message.code == code:
                return message.description
        raise ValueError("Invalid code")