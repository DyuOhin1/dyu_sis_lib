import base64

import requests

from icloud.constant.icloud_web_api import iCloudWebApi
from icloud.personal.utils.icloud_utils import iCloudUtils
from sis.connection import Connection, login_required


class CourseInformation:
    """
    歷年成績
    操行成績
    學期課表
    出缺席查詢
    """

    @staticmethod
    @login_required
    def annual_grade(
            conn : Connection
    ):
        data = iCloudUtils.fetch_record(
            iCloudWebApi.ANNUAL_GRADE,
            conn,
            "L0RhYXpsbElka1RMMmpCSi9lN3RnQT09"
        )

        return data

    @staticmethod
    @login_required
    def grade(
            conn : Connection,
            year: str,
            semester: str
    ):
        data = CourseInformation.annual_grade(conn)

        if not data["score"]:
            raise Exception("No data")

        for i in data["score"]:
            if i["year"] == year and i["sem"] == semester:
                return i

        raise Exception("No data for this year and semester")

    @staticmethod
    @login_required
    def performance_grade(
            conn : Connection
    ):
        res = requests.get(
            iCloudWebApi.PERFORMANCE_GRADE,
            cookies={
                "PHPSESSID": conn.php_session_id
            },
            params={
                "gGroups_i": 0,
                "gSys_s": "sis",
                "gFunc_s": "eWpDMnUvVkJnM1pjc3duWE4xMEJwZz09"
            }
        )

        if res.status_code < 200 or res.status_code >= 300:
            raise Exception("Failed to connect to the server")

        json_content = res.json()
        return json_content

    @staticmethod
    @login_required
    def timetable(
            conn: Connection,
            semester: str,
            grade: str
    ):
        data = iCloudUtils.fetch_record(
            iCloudWebApi.STUDENT_COURSE_TIMETABLE,
            conn,
            "N1MxdTc4V3ZBYm9sRTNjRDBWUUpyQT09",
            d = {
                "smye": semester,
                "smty": grade
            }
        )

        return data

    @staticmethod
    @login_required
    def timetable_pdf(
            conn: Connection,
            semester: str,
            grade: str
    ):
        rep = requests.get(
            iCloudWebApi.STUDENT_COURSE_TIMETABLE_PDF,
            cookies={
                "PHPSESSID": conn.php_session_id
            },
            params={
                "gGroups_i" : 0,
                "gSys_s": "sis",
                "gFunc_s": "N1MxdTc4V3ZBYm9sRTNjRDBWUUpyQT09",
                "smye": semester,
                "smty": grade
            }
        )

        if rep.status_code < 200 or rep.status_code >= 300:
            raise Exception("Failed to connect to the server")

        return base64.b64encode(rep.content).decode("utf-8")

    @staticmethod
    @login_required
    def attendance(
            conn: Connection
    ):
        data = iCloudUtils.fetch_record(
            iCloudWebApi.COURSE_ATTENDANCE,
            conn,
            "WlUwU2pCWis1WHNFSi9VOFk2SkJRQT09"
        )

        return data