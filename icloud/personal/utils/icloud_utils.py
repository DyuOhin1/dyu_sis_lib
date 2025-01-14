import json

from icloud.constant.icloud_web_api import iCloudWebApi
from sis.connection import Connection
import requests


class iCloudUtils:
    @staticmethod
    def student_semester(
            conn: Connection
    ):
        return iCloudUtils.fetch_record(
            iCloudWebApi.STUDENT_SEMESTER,
            conn,
            "N1MxdTc4V3ZBYm9sRTNjRDBWUUpyQT09"
        )

    @staticmethod
    def school_timetable():
        res = requests.get(
            iCloudWebApi.SCHOOL_TIMETABLE,
        )

        return iCloudUtils.parse_data(res, True)

    @staticmethod
    def parse_data(
            response : requests.Response,
            has_result: bool = True,
    ) -> json:
        """
        解析 JSON
        :param response:
        :param has_result:
        :return:
        """
        # 嘗試解析 JSON
        response.raise_for_status()
        json_content = response.json()

        # 如果不需要檢查 result，直接返回整個 JSON
        if not has_result:
            return json_content

        # 檢查 result 是否為 1
        if json_content.get("result") != 1:
            raise Exception(f"Failed to get record, msg: {json_content.get('msg', 'Unknown error')}")

        # 返回需要的資料部分
        return json_content.get("data")

    @staticmethod
    def fetch_record(
            endpoint: str,
            conn: Connection,
            g_func_s: str,
            has_result: bool = True,
            params: dict = None,
            d: dict = None
    ) -> json:
        """
        通用紀錄獲取方法
        :param endpoint: API 端點
        :param conn: 連線物件，包含 PHPSESSID
        :param g_func_s: 功能參數
        :param has_result: 是否需要檢查 result
        :param params: 其他參數
        :param d: 其他資料
        :return: JSON 資料
        """
        request_method = requests.post if d else requests.get

        # 發送請求
        response = request_method(
            endpoint,
            cookies={"PHPSESSID": conn.php_session_id},
            params={
                "gGroups_i": 0,
                "gSys_s": "sis",
                "gFunc_s": g_func_s,
                **(params or {})
            },
            data=d or {}
        )

        return iCloudUtils.parse_data(response, has_result)

