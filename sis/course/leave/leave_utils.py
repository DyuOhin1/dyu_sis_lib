import re

from bs4 import BeautifulSoup


class LeaveUtils:
    @staticmethod
    def parse_result_from_html(
            html: str
    ) -> dict[str, str]:
        """
        解析關於請假類型方面的結果
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all("script")

        result = {
            "success": False,
            "message": "Unknown error"
        }
        for script in scripts:
            if not script:
                continue
            match = re.search(r'alert\(["\'](.+?)["\']\)', script.text)
            if not match:
                continue
            alert_content = match.group(1)
            if "成功" in str(alert_content):
                result = {
                    "success": True,
                    "message": alert_content
                }
                break

        return result