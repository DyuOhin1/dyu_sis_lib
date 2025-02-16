import base64
import re
import time
from http.cookies import SimpleCookie

import requests
from bs4 import BeautifulSoup

from sis.constant.api import DyuWebAPI
from sis.course.leave.course_leave import CourseLeave as cl
from sis.exception import EmptyInputException, InvalidStudentIDException, InvalidPasswordException, ConnectionException, \
    AuthenticationException, RedirectException, HTTPRequestException, UnexpectedResponseException
from sis.personal.personal_information import PersonalInformation as pi
from sis.connection import Connection

""" 學生資訊系統 """
class StudentInformationSystem:
    course_leave = cl
    personal_info = pi

    @staticmethod
    def login(student_id, password):
        """
        使用 學號 跟 密碼 登入
        :param student_id: 學號
        :param password: 密碼
        :return: 登入後的 Connection 物件, 內包含 (學號, php session id, 上次登入時戳)
        """
        def prepare_login_params(sid, _pwd) -> dict[str, str]:
            """
            登入會將明文帳號密碼先 encode 成 utf8，再 base64 encode。
            :param sid: 學號
            :param _pwd: 密碼
            :return: base64 encoded student and password
            """

            # 判斷 sid 與 pwd 是否為空格或是空字串
            if sid.isspace() or _pwd.isspace() or not sid or not _pwd:
                raise EmptyInputException("Student ID or password cannot be empty")

            # 去除 sid 與 pwd 的特殊符號
            sid = sid.strip()
            _pwd = _pwd.strip()

            # 判斷 sid 與 pwd 是否合法，不合法則 raise exception
            if not re.match(r"^[A-Za-z]\d{7}$", sid):
                raise InvalidStudentIDException("Invalid student ID. Format: one letter followed by 7 digits.")

            if len(_pwd) < 8:
                raise InvalidPasswordException("Password is too short. Minimum length is 8 characters.")
            if len(_pwd) > 16:
                raise InvalidPasswordException("Password is too long. Maximum length is 16 characters.")

            sid = sid.encode("utf-8")
            _pwd = _pwd.encode("utf-8")
            url = "login_result.php".encode("utf-8")

            # base64 encode password ,student id and url
            s_id_base64 = base64.b64encode(sid).decode("utf-8")
            pwd_base64 = base64.b64encode(_pwd).decode("utf-8")
            url_base64 = base64.b64encode(url).decode("utf-8")

            return {
                "id": s_id_base64,
                "pwd": pwd_base64,
                "url": url_base64
            }

        def login_step_1(
                _para : dict[str, str]
        ) -> dict[str, str]:
            """
            登入第一步驟，將轉換成的 base64 code 以 url parameters 的方式 send get request，
            再轉址登入結果。
            :param _para: login parameters : 學號 , 密碼 and url
            :return: 回傳登入結果 url，登入成功與否都在此 url 顯示。
            """

            # 登入學生資訊系統 params from prepare_login_params()
            try:
                req = requests.get(DyuWebAPI.SIS_LOGIN, params=_para, timeout=100)
            except requests.Timeout:
                raise HTTPRequestException("Login step 1 failed due to timeout.")
            except requests.RequestException as e:
                raise HTTPRequestException(f"Login step 1 failed due to HTTP request error: {str(e)}")

            # 若登入失敗，則 raise exception
            if req.status_code < 200 or req.status_code >= 300:
                raise ConnectionException(f"Login step 1 failed, status code: {req.status_code}")

            # 取得登入後的 cookie，其中包含 PHPSESSID
            cookie = SimpleCookie(req.headers["Set-Cookie"])
            if "PHPSESSID" not in cookie:
                raise AuthenticationException("Login failed, PHPSESSID not found in cookies.")

            # 取得 meta content url，login 成功後會轉址到此 url
            soup = BeautifulSoup(req.text, "html.parser")
            # 取得 meta element
            meta_element = soup.find_all("meta")

            if not meta_element:
                raise UnexpectedResponseException("Login failed, meta tag not found in the response.")

            # 若 meta element 少於 2 則 raise exception，第二個 meta element 為轉址 url
            if len(meta_element) < 2:
                raise RedirectException("Login failed, redirect URL not found in meta content.")

            # 從第二個 meta element 取得 meta content url
            meta_content = meta_element[1]["content"]
            # 判斷 meta content 是否符合 '0; url=login_result.php?pass=t&name=%E7%8E%8B%E5%A4%A7%E6%98%8E'
            if not meta_content.startswith("0; url="):
                raise RedirectException("Login failed, please try again, redirect link not found")
            # 取得 url
            url = meta_content.split("url=")[1]

            phpsessid = cookie["PHPSESSID"].value
            if not phpsessid or not phpsessid.strip():
                raise AuthenticationException("Login failed, PHPSESSID is empty or invalid.")

            return {
                "url": url,
                "PHPSESSID": phpsessid
            }

        def login_step_2(
                url : str,
                phpsessid : str
        ) -> Connection:
            """
            登入成功則轉址，登入失敗則 throw exception
            :param url: 轉址 url
            :param phpsessid: php session id
            :return: Connection object
            """
            # https://sis.dyu.edu.tw/login_result.php?pass=f&error=1
            # pass=f 即登入失敗，丟出 exception
            if "error" in url:
                error_code = url.split("error=")[-1]
                raise AuthenticationException(f"Login failed with server error code: {error_code}.")

            # 使用登入後的 PHPSESSID 取得個人資訊表
            res = requests.get(url, cookies={"PHPSESSID": phpsessid})

            # 若登入失敗，則 raise exception
            if res.status_code < 200 or res.status_code >= 300:
                raise Exception(f"Login step 2 failed, please try again, status code: {res.status_code}")

            return Connection(student_id, phpsessid, time.time())


        para = prepare_login_params(student_id, password)  # base64 encode 帳號密碼及 url
        step_1_result = login_step_1(para)  # 取得登入後重新導向的 url 及 PHPSESSID
        login_result_url = DyuWebAPI.SIS_HOST + step_1_result["url"]  # 重新導向的 url
        return login_step_2(login_result_url, step_1_result["PHPSESSID"])

    @staticmethod
    def logout(
            conn : Connection
    ) -> None:
        res = requests.get(
            "https://sis.dyu.edu.tw/logout.php",
            cookies={
                "PHPSESSID": conn.php_session_id
            }
        )

        if res.status_code < 200 or res.status_code >= 300:
            raise Exception(f"Logout failed, please try again, status code: {res.status_code}")

        conn = None

    @staticmethod
    def is_logged_in(
            conn : Connection
    ) -> bool:
        res = requests.get(
            "https://sis.dyu.edu.tw/website_map.php?page=MQ==",
            cookies={
                "PHPSESSID": conn.php_session_id
            },
            timeout=5,
            allow_redirects=False
        )

        print(res.status_code)

        return res.status_code == 200