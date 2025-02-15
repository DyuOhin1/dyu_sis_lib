from functools import wraps
import time

from sis.exception import LoginSessionExpiredException


def login_required(method):
    """
    用於檢查是否登入，若未登入則拋出例外
    原理:
    1. 檢查是否有 Connection 實例
    2. 檢查是否登入

    :param method: 要檢查的方法
    """

    @wraps(method)
    def wrapper(*args, **kwargs):
        # 檢查是否有 Connection 實例
        connection = None
        for arg in args: # 檢查所有參數
            if isinstance(arg, Connection):
                connection = arg
                break

        if connection is None:
            raise ValueError("缺少 Connection 實例。")

        return method(*args, **kwargs)  # 呼叫原方法
    return wrapper

class Connection:
    def __init__(
            self,
            student_id : str,
            php_session_id : str,
            last_login_timestamp: float
    ):
        """
        保存學號、php session id、上次登入時戳物件，用於登入後的存取其他網頁服務
        :param student_id: 學號
        :param php_session_id: php session id
        :param last_login_timestamp: 登入時戳
        """

        self._student_id = student_id
        self._php_session_id = php_session_id
        self._last_login_timestamp = last_login_timestamp
        
    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, value):
        self._student_id = value

    @property
    def php_session_id(self):
        return self._php_session_id

    @php_session_id.setter
    def php_session_id(self, value):
        self._php_session_id = value

    @property
    def last_login_timestamp(self):
        return self._last_login_timestamp

    @last_login_timestamp.setter
    def last_login_timestamp(self, value):
        self._last_login_timestamp = value