import base64
from enum import Enum
from typing import Dict, Union, List, Any, Optional

import requests
from bs4 import BeautifulSoup

from sis.connection import login_required, Connection
from sis.constant.api import DyuWebAPI
from sis.personal.modals.graduation.computer_graduation import ComputerGraduation
from sis.personal.modals.graduation.language_graduation import LanguageGraduation
from sis.personal.personal_untils import PersonalUtils

class FetchType(Enum):
    ENGLISH = "ENGLISH"
    CHINESE = "CHINESE"
    COMPUTER = "COMPUTER"

class Graduation:
    """
    畢業資訊
    """

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
    def __get_language_cert_by_source_html(
            source_html: str,
            fetch_type : FetchType,
            table_content_id_prefix : str = "it",
            table_result_id : str = "table_result"
    ) -> dict[str, Union[list[Any], dict[str, Union[str, Any]]]]:
        def get_graduation(data: list[str]) -> Union[LanguageGraduation, ComputerGraduation]:
            fetch_type_map = {
                FetchType.ENGLISH: lambda : LanguageGraduation(
                    id=data[0],
                    year=data[1][:3],
                    semester=data[1][3:4],
                    title=data[2],
                    score=data[4],
                    issuer=data[3]
                ),
                FetchType.CHINESE: lambda : LanguageGraduation(
                    id=data[0],
                    year=data[1],
                    semester=data[2],
                    title=data[3],
                    score=data[4],
                ),
                FetchType.COMPUTER: lambda : ComputerGraduation(
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

    @staticmethod
    @login_required
    def info(
            conn: Connection
    ) -> list[Union[dict[str, Any], dict[str, dict[str, Any]]]]:
        """
        取得畢業資訊，包含畢業標準、已修學分、修課中學分、尚缺學分
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

        return [
            dict(zip(titles, required_credit)),
            dict(zip(titles, earned_credit)),
            dict(zip(titles, in_progress_credit)),
            dict(zip(titles, missing_credit))
        ]

