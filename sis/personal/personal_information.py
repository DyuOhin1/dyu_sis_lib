import base64
import json
import re
from typing import Any, Generator

import requests

from icloud.constant.icloud_web_api import iCloudWebApi
from sis.connection import login_required, Connection
from sis.constant.api import DyuWebAPI
from sis.personal import info_map
from bs4 import BeautifulSoup

from sis.personal.modals.course_warning_DTO import CourseWarningDTO
from sis.personal.modals.injury_record import InjuryRecord

# TODO: add exception handling
"""
大多核心功能已完成，但還有一些功能需要實作，例如：
- 學生證內外號碼資訊
考慮製作:
- 汽機車通行證
- 工讀資訊
- 成績文件申請
"""
class PersonalInformation:

    @staticmethod
    def personal_course_list_pdf(
            s_id: str,
            semester: str,
            semester_grade : str,
    ) -> str:
        """
        取得修課清單 PDF
        :param s_id: 學號
        :param semester: 學期
        :param semester_grade: 年級
        :return: str
        """
        req = requests.get(
            DyuWebAPI.SIS_PERSONAL_COURSE_LIST,
            params={
                "stno": s_id,
                "smye": semester,
                "smty": semester_grade
            }
        )

        return base64.b64encode(req.content).decode("utf-8")

    @staticmethod
    def personal_barcode(
        s_id: str,
        width: int = 300,
        height: int = 130,
        use_in_html: bool = False,
        image_format: str = "png"
    ) -> str:
        # 發送 GET 請求取得圖片的二進位內容
        response = requests.get(
            "https://itc.dyu.edu.tw/barcode/barcode.php",
            params={
                "barcode": s_id,
                "width": width,
                "height": height,
                "format": "png"
            }
        )

        # 將圖片內容轉換為 Base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')

        # 加上 data URI 前綴 (可直接在 HTML 使用)
        return f"data:image/{image_format};base64,{image_base64}" if use_in_html else image_base64

    @staticmethod
    def personal_image(
        s_id: str,
        type: int = 3,
        prgtype: int = 8
    ) -> str:
        req = requests.get(
            iCloudWebApi.PERSONAL_IMAGE,
            params={
                "pid": f"\"{s_id}\"",
                "type": type,
                "prgtype" : prgtype
            }
        )

        json_data = req.json()

        if json_data["result"] != 1:
            raise Exception("Failed to get personal image")
        if json_data['data'][s_id]['image_type'] == 0:
            raise Exception(f"{s_id} personal image not found")

        base64_str = json_data['data'][s_id]['image']
        encoded = base64_str.split(",")[1]

        return encoded

    @staticmethod
    @login_required
    def graduation_pdf(
        conn : Connection
    ) -> str:
        """
        取得畢業資訊 PDF
        """
        req = requests.get(
            DyuWebAPI.SIS_GRADUATION_INFO_PDF,
            cookies={
                "PHPSESSID": conn.php_session_id
            }
        )

        return base64.b64encode(req.content).decode("utf-8")

    @staticmethod
    @login_required
    def graduation(
        conn: Connection
    ) -> dict:
        """
        取得畢業資訊
        """
        def parse_credits(credit_section):
            return [
                {
                    "credit": credit.contents[3].text,
                    "count": credit.contents[1].text.strip("()")
                }
                for credit in credit_section.contents[1:]
            ]

        req = requests.get(
            DyuWebAPI.SIS_GRADUATION_INFO,
            cookies={"PHPSESSID": conn.php_session_id}
        )

        soup = BeautifulSoup(req.text, "html.parser")

        titles = [
            t.get_text(strip=True)
            for t in soup.find("div", class_="title row-ex")
            if t.get_text(strip=True)
        ]

        context = soup.find("div", class_="context")

        required_credit = [
            credit.get_text(strip=True)
            for credit in context.contents[1]
            if credit.get_text(strip=True).isdigit()
        ]
        required_credit.append("-")

        earned_credit = parse_credits(context.contents[2])
        in_progress_credit = parse_credits(context.contents[3])
        missing_credit = parse_credits(context.contents[4])

        return {
            "title": titles,
            "required": required_credit,
            "earned": earned_credit,
            "in_process": in_progress_credit,
            "missing": missing_credit
        }

    @staticmethod
    @login_required
    def course_warning(
            conn : Connection
    ) -> list[CourseWarningDTO]:
        course_warning_row = PersonalInformation.__fetch_and_parse(
            conn,
            start=1,
            end=8
        )

        return [
            CourseWarningDTO.from_source(
                row[0],  # 科目序號
                row[1],  # 科目名稱
                row[2],  # 修別
                row[3],  # 教師姓名
                row[4],  # 預警情形
                row[5],  # 學分數
                row[6],  # 備註
            )
            for row in course_warning_row
        ]

    @staticmethod
    @login_required
    def injury_record(
            conn : Connection
    ) -> Generator[InjuryRecord, None, None]:
        """
        取得傷害紀錄
        :param conn: Connection object with php session id
        :return: dict
        """
        injury_row_list = PersonalInformation.__fetch_and_parse(
            DyuWebAPI.SIS_INJURY_RECORD,
            conn,
            start=1,
            end=8
        )

        return (
            InjuryRecord.from_source(
                row[0],  # 學年期
                row[1],  # 發生時間
                row[2],  # 校內/校外
                row[3],  # 事件
                row[4],  # 地點
                row[5],  # 受傷部位
                row[6],  # 後續處理
                row[7]   # 備註
            )
            for row in injury_row_list if len(row) != 0
        )

    @staticmethod
    @login_required
    def privacy(
            conn : Connection
    ) -> json:
        """
        利用登入後的 php session id 取得個人資訊表，再利用 regex 解析 js code 裡面的 variables
        這些 js code variables be like:
        data[data.length] = "王大明";//姓名
        data[data.length] = "1";//性別
        data[data.length] = "A123456789";//身分證字號
        data[data.length] = "111年11月11日";//生日
        data[data.length] = "3";//經濟狀況
        data[data.length] = "0";//身分別
        data[data.length] = "";//聯絡電話
        ...

        :param conn: Connection object with php session id
        :return: dict[str, str]
        """

        # 抓取個人資訊
        req = requests.get(
            DyuWebAPI.SIS_PERSONAL_INFO,
            cookies={"PHPSESSID": conn.php_session_id}
        )

        if req.status_code < 200 or req.status_code >= 300:
            raise Exception(f"Get student info failed, please try again, status code: {req.status_code}")

        # 轉碼成 utf-8
        req.encoding = "utf-8"
        # 個人資訊格式 be like data[data.length] = "王大明";//姓名
        pattern = r'^data\[data\.length\] = "(.*?)";\s*//\s*(.*)$'

        # 找尋所有符合條件的所有格式並包裝成一個 array
        info = re.findall(pattern, req.text, re.MULTILINE)

        if len(info) == 0:
            raise Exception("No student info found")

        info = [match[0].strip() for match in info]

        # return 並轉會成 json data
        return info_map.convert(info)

    @staticmethod
    @login_required
    def __fetch_and_parse(
            url: str,
            conn: Connection,
            start: int,
            end: int
    ) -> list[list[str]]:
        """
        發送請求並解析 class=row 的內容。

        :param url: 請求的 URL
        :param conn: Connection object with PHP session ID
        :param start: 欄位起始索引
        :param end: 欄位結束索引
        :return: 解析後的內容列表，每一列是 list[str]
        """

        def get_row_content(
                s_i: int,
                e_i: int,
                raw_html_content: str,
                strip_str: bool = True
        ) -> list[list]:
            """

            """
            soup = BeautifulSoup(raw_html_content, "html.parser")
            content = soup.find_all("div", class_="row")

            return [
                [
                    cell.get_text(strip=strip_str)
                    for i in range(s_i, e_i + 1)
                    if (cell := row.find('div', class_=f'column{i}'))
                ]
                for row in content
            ]

        # 發送 HTTP GET 請求
        req = requests.get(
            url,
            cookies={"PHPSESSID": conn.php_session_id}
        )

        # 檢查回應狀態碼
        if req.status_code < 200 or req.status_code >= 300:
            raise Exception(f"Request failed, status code: {req.status_code}")

        req.encoding = "utf-8"

        # 取得並解析 row 內容
        return get_row_content(start, end, req.text)