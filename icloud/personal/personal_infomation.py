import base64
import json
from textwrap import dedent
from urllib.parse import urlencode

import requests

from icloud.constant.icloud_web_api import iCloudWebApi
from icloud.personal.constants.lang import Lang
from icloud.personal.constants.printer_error_code import PrinterErrorCode
from icloud.personal.utils.icloud_utils import iCloudUtils
from sis.connection import Connection, login_required


class PersonalInformation:
    @staticmethod
    @login_required
    def military_record(
            conn: Connection
    ) -> json:
        """
        兵役紀錄
        """
        return iCloudUtils.fetch_record(
            iCloudWebApi.MILITARY_RECORD,
            conn,
            "MjRTMlVyN0FiWVk5cktxZlFGS211dz09"
        )

    @staticmethod
    @login_required
    def injury_record(
            conn: Connection
    ):
        """
        受傷紀錄
        """
        return iCloudUtils.fetch_record(
            iCloudWebApi.INJURY_RECORD,
            conn,
            "S2twSkVlYmswWXhSQ2NzMjVhK2RIZz09"
        )

    @staticmethod
    @login_required
    def advisors(
            conn: Connection,
    ):
        """
        我的導師
        """
        data = iCloudUtils.fetch_record(
            iCloudWebApi.ADVISORS,
            conn,
            "d2ZaN2RRelV5N1gxRncwL2hXaW1rZz09"
        )

        # data be like {"year":113,"sem":1,"teno":"asdasd","epno":"dasdasd","tutor_status":"A"}
        return data

    @staticmethod
    @login_required
    def rewards_and_penalties_record(
            conn: Connection
    ):
        """
        獎懲紀錄
        """
        return iCloudUtils.fetch_record(
            iCloudWebApi.REWARDS_AND_PENALTIES_RECORD,
            conn,
            "VkJaeGQvSXkvMnZ1Z3lIbU1Cb2F4dz09",
            has_result=False
        )

    @staticmethod
    @login_required
    def proof_of_enrollment_pdf(
            conn: Connection,
            semester: str,
            grade: str,
    ) -> str:
        data = PersonalInformation.proof_of_enrollment(
            conn,
            is_preview=True
        )

        for detail in data['detail']:
            if str(detail['smye']) != semester or str(detail['smty']) != grade or not bool(detail['isPay']):
                continue

            res = requests.get(
                detail['pdf'],
                cookies= {
                    "PHPSESSID": conn.php_session_id
                }
            )

            return base64.b64encode(res.content).decode("utf-8")
        raise Exception("No such record")

    @staticmethod
    @login_required
    def proof_of_enrollment(
        conn : Connection,
        is_preview: bool = False,
        lang : Lang = Lang.ZH_TW
    ):
        """
        在學證明
        """
        data = iCloudUtils.fetch_record(
            iCloudWebApi.PROOF_OF_ENROLL,
            conn,
            "dloySHhpRzdEVzR4SlVoVUZLR0xyQT09",
            d={
                "lang": lang.value
            }
        )

        pic = data['picture_url']
        if not is_preview and data['picture_url']:
            data['picture_url'] =  pic.split(",")[1]

        details = data['detail']

        for detail in details:
            params = {
                "gGroups_i": 0,
                "gSys_s": "sis",
                "gFunc_s": "dloySHhpRzdEVzR4SlVoVUZLR0xyQT09",
                "smye": detail['smye'],
                "smty": detail['smty'],
                "id": detail['stno_encode'],
            }
            detail['pdf'] = f"{iCloudWebApi.PROOF_OF_ENROLL_PDF}?{urlencode(params)}"

        return data

    @staticmethod
    @login_required
    def scholarship_record(
        conn : Connection
    ):
        """
        獎學金紀錄
        """
        return iCloudUtils.fetch_record(
            iCloudWebApi.SCHOLARSHIP_RECORD,
            conn,
            "RTl4Vmo0clhIRHpHWDhUaEE0b3Y4UT09"
        )

    @staticmethod
    @login_required
    def printer_point(
            conn : Connection
    ):
        """
        列印點數
        """
        res = requests.post(
            iCloudWebApi.PRINTER_POINT,
            cookies= {
                "PHPSESSID": conn.php_session_id
            },
            params= {
                "gGroups_i": 0,
                "gSys_s": "sis",
                "gFunc_s": "QXBKNm9Hd1JJRVhZcFpvVEMxNVhvQT09"
            }
        )

        json_content = res.json()
        if json_content["errcode"] != 0:
            error_code = json_content["errcode"]
            error_message = PrinterErrorCode.get_description_by_code(error_code)
            raise Exception(f"Failed to get printer point, return_error_msg: {json_content['errtext']}, error_msg: {error_message}")

        point = json_content["point"]
        if point.startswith("\ufeff"):
            point = point[1:]

        if not point.isdigit():
            raise Exception(f"Failed to get printer point, error: unknown error, point: {point}")

        return int(point)

    @staticmethod
    @login_required
    def dorm_record(
            conn : Connection
    ) -> json:
        """
        住宿紀錄
        """
        return iCloudUtils.fetch_record(
            iCloudWebApi.DORM_RECORD,
            conn,
            "YUNyTmV0Q3F0UGpWVUlDNU1VVjl3dz09"
        )