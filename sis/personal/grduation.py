import base64
from typing import Dict, Union, List, Any

import requests
from bs4 import BeautifulSoup

from sis.connection import login_required, Connection
from sis.constant.api import DyuWebAPI
from sis.personal.personal_untils import PersonalUtils


class Graduation:
    """
    畢業資訊
    """

    @staticmethod
    @login_required
    def info_certification(
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

        soup = BeautifulSoup(res.text, "html.parser")
        content_row = soup.find_all("div", class_="row")
        content_result = soup.find("div", class_="row_click")

        keys = ["id", "name", "cert_number", "issuer", "date", "semester"]

        value = (
            (i for j in row if (i := j.get_text(strip=True)))
            for row in content_row
            if len(row) == len(content_row[0])
        )
        result = PersonalUtils.get_row_content(content_result)

        return {
            "data" : [dict(zip(keys, row)) for row in value],
            "passable": {
                "title" : result[0],
                "result" : result[1],
            }
        }

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

