from collections.abc import Iterable

import requests
from bs4 import BeautifulSoup, Tag

from sis.connection import login_required, Connection


class PersonalUtils:
    @staticmethod
    @login_required
    def fetch_and_parse(
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

    @staticmethod
    def raise_check(
            content : Iterable[Tag]
    ) -> None:
        for i in content:
            if not i:
                raise Exception("info_certification No content found")
            if not hasattr(i, "children"):
                raise Exception("info_certification No content found(can not find children)")

    @staticmethod
    def get_row_content(
            content : Tag
    ) -> list[str]:
        return [
            cell
            for row in content.children
            if (cell := row.get_text(strip=True))
        ]