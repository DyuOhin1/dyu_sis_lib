class LoginException(Exception):
    """通用登入錯誤"""
    pass

class EmptyInputException(LoginException):
    """學號或密碼為空"""
    pass

class InvalidStudentIDException(LoginException):
    """學號格式錯誤"""
    pass

class InvalidPasswordException(LoginException):
    """密碼格式錯誤"""
    pass

class ConnectionException(LoginException):
    """連線錯誤，例如伺服器無法存取"""
    pass

class RedirectException(LoginException):
    """重新導向錯誤"""
    pass

class AuthenticationException(LoginException):
    """驗證失敗"""
    pass

class HTTPRequestException(ConnectionException):
    """HTTP 請求錯誤"""
    pass

class UnexpectedResponseException(AuthenticationException):
    """伺服器回應格式不符"""
    pass

