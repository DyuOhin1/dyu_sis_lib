import base64
import re
import time
from http.cookies import SimpleCookie

import requests

from icloud.constant.icloud_web_api import iCloudWebApi
from icloud.course.course_information import CourseInformation
from icloud.personal.personal_infomation import PersonalInformation
from icloud.personal.utils.icloud_utils import iCloudUtils
from sis.connection import Connection, login_required


class iCloud:
    personal_information = PersonalInformation
    course_information = CourseInformation

    @staticmethod
    @login_required
    def advisor_info(
            conn: Connection,
            teno: str
    ):
        if not teno:
            raise Exception("Advisor's teno is empty")

        teacher_data = iCloudUtils.fetch_record(
            iCloudWebApi.ADVISOR_INFO,
            conn,
            "d2ZaN2RRelV5N1gxRncwL2hXaW1rZz09",
            params={
                "teno": teno
            }
        )

        for i in teacher_data:
            if not i["img"]:
                break
            i["img"] = i["img"].split(",")[1]

        return teacher_data

    @staticmethod
    def __get_connection_by_response(
            s_id : str,
            res : requests.Response
    ):
        if res.status_code < 200 or res.status_code >= 300:
            raise Exception("Failed to connect to the server")

        match = re.search(r'alert\("(.+?)"\)', res.text, re.DOTALL)

        if match:
            alert_message = match.group(1)
            raise Exception(alert_message)

        cookie = SimpleCookie(res.headers["Set-Cookie"])
        return Connection(
            student_id= s_id,
            php_session_id= cookie["PHPSESSID"].value,
            last_login_timestamp= time.time()
        )

    @staticmethod
    def login(
            acc : str,
            pwd : str,
    ) -> Connection:
        res = requests.post(
            iCloudWebApi.LOGIN,
            data= {
                "acc" : acc,
                "pwd" : pwd
            }
        )

        return iCloud.__get_connection_by_response(
            acc,
            res
        )

    @staticmethod
    def login_with_token(
            s_id : str,
            token : str
    ):
        res = requests.get(
            iCloudWebApi.LOGIN,
            params= {
                "data": token
            }
        )

        return iCloud.__get_connection_by_response(
            s_id,
            res
        )

    @staticmethod
    @login_required
    def logout(
            conn: Connection
    ):
        response = requests.get(
            iCloudWebApi.LOGOUT,
            cookies={
                "PHPSESSID": conn.php_session_id
            }
        )

        if response.status_code == 200 or response.status_code == 302:
            return True
        else:
            raise Exception(f"""
                     Failed to logout, code: {response.status_code},
                     content: {response.text}
                    """)