import base64
from enum import Enum
from typing import Dict, Union, List, Any, Optional

import requests
from bs4 import BeautifulSoup, Tag

from sis.connection import login_required, Connection
from sis.constant.api import DyuWebAPI
from sis.personal.modals.graduation.computer_graduation import ComputerGraduation
from sis.personal.modals.graduation.language_graduation import LanguageGraduation
from sis.personal.modals.graduation.working_project import WorkingProject
from sis.personal.personal_untils import PersonalUtils

class FetchType(Enum):
    ENGLISH = "ENGLISH"
    CHINESE = "CHINESE"
    COMPUTER = "COMPUTER"

class Graduation:
    """
    畢業資訊
    """

    from typing import List, Dict
    from bs4 import BeautifulSoup, Tag

    @staticmethod
    @login_required
    def workplace_exp(
            conn: Connection
    ):
        res = requests.get(
            "https://sis.dyu.edu.tw/page_system.php?page=MzQ=",
            cookies={"PHPSESSID": conn.php_session_id}
        )

        res.encoding = "utf-8"

        soup = BeautifulSoup(res.text, "html.parser")

        content = soup.find("div", id="conduct_content")

        title = []
        projects = []
        for child in content.children:
            if not child.get_text(strip=True):
                continue

            project = PersonalUtils.get_row_content(child)

            if "明細" in project[-1]:
                details = child.contents[-1]
                details_id = details.get("onclick")[-2]
                projects.append(
                    WorkingProject(
                        id=details_id,
                        title=project[0],
                        max_hours=int(project[1]),
                        total_hours=int(project[2]),
                        cert_hours=int(project[3]),
                        detail_link=Graduation._get_working_details_link(int(details_id))
                    ).to_dict()
                )
            else:
                title.append(
                    {
                        "title": project[0],
                        "cert": project[1],
                        "total": project[2],
                        None if len(projects) == 0 else "projects": projects
                    }
                )
                projects = []
        return title

    @staticmethod
    def _get_working_details_link(details_id: int) -> str:
        """
        Get the details link for a working project based on the details ID.

        Args:
            details_id (int): The ID of the detail (range: 0-8).

        Returns:
            str: The URL corresponding to the details ID.

        Raises:
            ValueError: If details_id is out of the valid range (0-8).
        """
        # Validate the details ID
        if not (0 <= details_id <= 8):
            raise ValueError("Invalid details ID. Allowed range: 0-8")

        # Define a mapping for specific IDs
        special_links = {
            5: "graduation_info/work_hour.php?item=5",
            6: "graduation_info/career_hour.php?item=6",
            7: "graduation_info/industry_hour.php?item=7",
            8: "graduation_info/compete_hour.php?item=8",
        }

        # Return the link for IDs 0-4 or the specific mapping for IDs 5-8
        if details_id <= 4:
            return f"graduation_info/work_place.php?item={details_id}"
        return special_links.get(details_id)

    @staticmethod
    @login_required
    def english(
            conn: Connection
    ):
        res = requests.get(
            "https://sis.dyu.edu.tw/page_system.php?page=MzI=",
            cookies={"PHPSESSID": conn.php_session_id}
        )

        res.encoding = "utf-8"
        return Graduation.__get_language_cert_by_source_html(
            res.text,
            FetchType.ENGLISH
        )

    @staticmethod
    @login_required
    def chinese(
            conn : Connection
    ) -> dict[str, Union[list[dict[str, Any]], dict[str, Any]]]:
        res = requests.get(
            "https://sis.dyu.edu.tw/page_system.php?page=MzE=",
            cookies={"PHPSESSID": conn.php_session_id}
        )
        res.encoding = "utf-8"
        return Graduation.__get_language_cert_by_source_html(
            res.text,
            FetchType.CHINESE
        )

    @staticmethod
    @login_required
    def computer(
            conn: Connection
    ) -> dict[str, Union[list[dict[str, Any]], dict[str, Any]]]:
        """
        取得畢業資訊證明
        """

        res = requests.get(
            DyuWebAPI.SIS_GRADUATION_INFO_CERTIFICATION,
            cookies={"PHPSESSID": conn.php_session_id}
        )

        res.encoding = "utf-8"

        return Graduation.__get_language_cert_by_source_html(
            res.text,
            FetchType.COMPUTER,
            table_result_id="row_click"
        )

    @staticmethod
    @login_required
    def pdf(
            conn: Connection
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
    """
    uni_req → University Required
    col_req → College Required
    dep_req → Department Required
    dep_elec → Department Elective
    free_req → Free Required
    free_elec → Free Elective
    total → Total Credits
    uncat → Uncategorized Credits
    """
    info_titles = [
        "uni_req",
        "col_req",
        "dep_req",
        "dep_elec",
        "free_req",
        "free_elec",
        "total",
        "uncat",
    ]

    @staticmethod
    @login_required
    def info(conn: Connection) -> dict[str, dict[str, int]]:
        """
        取得畢業資訊：
        - `req`: 應修學分
        - `earned`: 已修學分
        - `count`: 修課數量
        - `in_progress`: 修習中學分
        - `missing`: 缺修學分
        """

        def parse_credits(credit_section):
            """解析學分數據，處理 `"-"` 和括號內數字"""
            return [
                {
                    "credit": int(credit.contents[3].text.strip()) if credit.contents[3].text.strip(
                        "-").isdigit() else 0,
                    "count": int(credit.contents[1].text.strip("()")) if credit.contents[1].text.strip(
                        "()").isdigit() else 0
                }
                for credit in credit_section.contents[1:]
            ]

        # **請求 SIS 畢業資訊**
        req = requests.get(
            DyuWebAPI.SIS_GRADUATION_INFO,
            cookies={"PHPSESSID": conn.php_session_id}
        )
        soup = BeautifulSoup(req.text, "html.parser")
        context = soup.find("div", class_="context")

        # **確保 `titles` 的順序**
        titles = [
            t.get_text(strip=True)
            for t in soup.find("div", class_="title row-ex")
            if t.get_text(strip=True)
        ]

        #  解析應修學分數
        required_credit = [
            int(credit.get_text(strip=True))
            for credit in context.contents[1]
            if credit.get_text(strip=True).isdigit()
        ]
        required_credit.append(0)  # 確保 `uncat` 為 0

        # 解析已修、修習中、缺修學分
        earned_credit = parse_credits(context.contents[2])
        in_progress_credit = parse_credits(context.contents[3])
        missing_credit = parse_credits(context.contents[4])

        # 確保所有數據匹配
        result = {}
        for idx, key in enumerate(Graduation.info_titles):
            result[key] = {
                "req": required_credit[idx],  # ✅ 確保 `req` 正確
                "earned": earned_credit[idx]["credit"],
                "count": earned_credit[idx]["count"],
                "in_progress": in_progress_credit[idx]["credit"],
                "missing": missing_credit[idx]["credit"],
            }

        return result


    @staticmethod
    def __get_language_cert_by_source_html(
            source_html: str,
            fetch_type: FetchType,
            table_content_id_prefix: str = "it",
            table_result_id: str = "table_result"
    ) -> dict[str, Union[list[Any], dict[str, Union[str, Any]]]]:
        def get_graduation(data: list[str]) -> Union[LanguageGraduation, ComputerGraduation]:
            fetch_type_map = {
                FetchType.ENGLISH: lambda: LanguageGraduation(
                    id=data[0],
                    year=data[1][:3],
                    semester=data[1][3:4],
                    title=data[2],
                    score=data[4],
                    issuer=data[3]
                ),
                FetchType.CHINESE: lambda: LanguageGraduation(
                    id=data[0],
                    year=data[1],
                    semester=data[2],
                    title=data[3],
                    score=data[4],
                ),
                FetchType.COMPUTER: lambda: ComputerGraduation(
                    id=data[0],
                    year=data[5][:3],
                    semester=data[5][3:4],
                    title=data[1],
                    cert_id=data[2],
                    issuer=data[3],
                    cert_date=data[4]
                )
            }

            try:
                return fetch_type_map[fetch_type]()
            except KeyError:
                raise Exception("Invalid fetch type")

        soup = BeautifulSoup(source_html, "html.parser")

        count = 1
        return_data = []
        while row := soup.find("div", id=f"{table_content_id_prefix}{count}"):
            data = PersonalUtils.get_row_content(row)
            return_data.append(
                get_graduation(data)
            )
            count += 1

        row = soup.find("div", id=table_result_id) or \
              soup.find("div", class_=table_result_id)
        result = PersonalUtils.get_row_content(row)

        return {
            "data": [row.to_dict() for row in return_data],
            "passable": {
                "title": result[0],
                "result": "通過" if "通過" in result[1] else "不通過"
            }
        }