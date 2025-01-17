import re
from datetime import date, datetime
from typing import List, BinaryIO

import requests
from bs4 import BeautifulSoup

from sis.connection import Connection, login_required
from sis.constant.api import DyuWebAPI
from sis.course.leave.constant.leave_result import LeaveResult
from sis.course.leave.leave_utils import LeaveUtils
from sis.modals.course import CourseWithDate
from sis.course.leave.modals.leave_data import LeaveData
from sis.course.leave.modals.leave_detail import LeaveDetail
from sis.course.leave.modals.leave_form_data.leave_form_data import LeaveFormData
from sis.modals.teacher import Teacher


class CourseLeave:
    @staticmethod
    @login_required
    def submit_document(
            conn: Connection,
            leave_id : str,
            file: BinaryIO
    ) -> dict[str, str]:
        """
        提交請假證明文件
        :param conn:
        :param leave_id: 請假編號
        :param file: 證明文件
        :return: dict[str, str]
        """

        # 提交請假證明文件，docid 為請假編號，php session id 為登入後的 session id，用於驗證身分
        res = requests.post(
            DyuWebAPI.SIS_LEAVE_SUBMIT_DOC,
            files={"path": file},
            data={"vac_id": leave_id},
            cookies={"PHPSESSID": conn.php_session_id}
        )

        if res.status_code < 200 or res.status_code >= 300:
            raise Exception(f"Submit document failed, status code: {res.status_code}")

        res.encoding = 'utf-8'
        return LeaveUtils.parse_result_from_html(
            res.text
        )


    @staticmethod
    @login_required
    def send(
            conn : Connection,
            leave_form_data: LeaveFormData
    ) -> LeaveResult:
        """
        送出請假請求， LeaveFormData 共有兩種類型，分別為 CourseLeaveFormData 跟 MeetingLeaveFormData：
        - CourseLeaveFormData: 普通上課請假 FormData
            必須使用 CourseLeave.info() 來取得課程資訊(CourseWithDate)，再過濾出要請假的課程，再將其傳入 CourseLeaveFormData 建構此物件

        - MeetingLeaveFormData: 重要集會請假 FormData

        :param conn: Connection
        :param leave_form_data:
        :return: requests.Response
        """

        # 取得請假資料
        post_data = leave_form_data.to_form_data()

        # 送出請假資料
        rep = requests.post(
            leave_form_data.request_url, # 請假網址
            data=post_data["data"], # 請假資料
            files=post_data["file"], # 證明文件
            cookies={"PHPSESSID": conn.php_session_id} # 登入後的 PHP session id
        )

        def get_leave_result(rep : requests.Response):
            """
            解析請假結果 (成功/失敗)
            """

            # 解析整夜並轉換成 BeautifulSoup 物件
            soup = BeautifulSoup(rep.text, "html.parser")

            """
            其中網頁部分 html(含請假結果的)：
            ```
            <!-- 部分省略 -->
            <script language="JavaScript" type="text/javascript">
                function success() {
                    alert("請假完成。\r\n學生線上系統請假請記得隨時注意假單審核狀況。\r\n如假單未審核，請記得提醒跟催老師。");
                    <!-- 部分省略 -->
                }
                function fail2() {
                    alert("請假失敗，系統繁忙中請稍後再試。");
                    <!-- 部分省略 -->
                }
                function fail() {
                    alert("請假失敗！\n可能原因有：\n1.證明文件的檔案大小超過2M(解決辦法：將證明文件縮減至2M以下)\n2.閒置過久(解決辦法：請重新登入)。");
                    <!-- 部分省略 -->
                }
                function error_message( error_msg ) {
                    if( error_msg == 3 ) { 
                        alert("上傳檔案錯誤！\n原因：檔案僅被部分上傳。");
                    }
                    if( error_msg == 4) { 
                        alert("上傳檔案錯誤！\n原因：檔案未被上傳。");
                    } else { 
                        alert("上傳檔案錯誤！\n原因：檔案上傳大小限制為2M。");
                    }
                    history.go(-1);
                }
            </script>
            <!-- 部分省略 -->
            <script language="JavaScript" type="text/javascript">success();</script>
            <!-- 部分省略 -->
            ```
            因此需要抓取 <script> element 中的資料，知道呼叫了哪個 function，在依照 function name 來判斷請假是否成功。
            其中有一個 function 是 error_message，這個 function 會根據 error_msg 來判斷錯誤原因，error_msg 依照 function 內部來看，應該是整數。
            因此不只要抓取 function name，也抓取 function parameter。
            """

            # 取得請假結果，請求後的訊息放在 <script> element 中
            script = soup.find_all("script")
            if len(script) < 2:
                raise Exception("Can not find leave result script element")

            message_script = script[1]
            # 使用正規表達式取得請假結果，包含 function name 和 function parameter
            pattern = r"(\w+)\s*\((.*?)\)"
            # 取得所有請假結果
            matches = re.findall(pattern, message_script.text)

            """
            這邊的 matches 會是一個 list，裡面的元素是 tuple，tuple 的第一個元素是 function name，第二個元素是 function parameter。
            matches = [('success', '')]
            """

            if len(matches) == 0 or len(matches[0]) == 0:
                raise Exception("Can not find leave result")

            # 抓取 function name
            key = matches[0][0]
            # 抓取 function parameter
            code = matches[0][1]
            return LeaveResult.from_key(key, code)

        return get_leave_result(rep)

    @staticmethod
    @login_required
    def cancel(
            conn : Connection,
            leave_id : str
    ) -> dict[str, str]:
        """
        取消請假
        :param conn: Connection
        :param leave_id: 請假編號
        :return: requests.Response
        """

        # 取消請假，docid 為請假編號，php session id 為登入後的 session id，用於驗證身分
        res = requests.get(
            f"{DyuWebAPI.SIS_LEAVE_CANCEL}?docid={leave_id}",
            cookies={"PHPSESSID": conn.php_session_id}
        )

        if res.status_code < 200 or res.status_code >= 300:
            raise Exception(f"Cancel leave failed, status code: {res.status_code}")

        res.encoding = 'utf-8'
        return LeaveUtils.parse_result_from_html(
            res.text
        )


    @staticmethod
    @login_required
    def detail(
            conn: Connection,
            leave_data : LeaveData
    ):
        """
        取得請假詳細資訊
        :param conn: Connection
        :param leave_data: LeaveData
        :return: LeaveData
        """

        # 取得請假詳細資訊，doc_id 為請假編號，php session id 為登入後的 session id，用於驗證身分
        res = requests.get(
            f"{DyuWebAPI.SIS_LEAVE_DETAIL}?doc_id={leave_data.id}",
            cookies={"PHPSESSID": conn.php_session_id}
        )

        # Response 轉碼成 utf-8
        res.encoding = "utf-8"

        # 請假詳細資訊格式 be like leave_Info[0] = new Array("2021/09/01", "1", "課程名稱", "審核人", "關係", "審核狀態", "審核日期", "集會名稱", "宿舍集會名稱", "審核說明", "請假訊息");
        info_pattern = r'leave_Info\[[^\]]+\] = new Array\("(.*?)", "(.*?)", "(.*?)", "(.*?)", "(.*?)", "(.*?)", "(.*?)", "(.*?)", "(.*?)", "(.*?)", "(.*?)"\);'

        # 取得請假詳細資訊 matches，內容為 tuple，會包含 日期、課程名稱、審核人、關係、審核狀態、審核日期、集會名稱、宿舍集會名稱、審核說明。
        info_matches = re.findall(info_pattern, res.text)

        # 若無請假詳細資訊，則 raise exception
        if len(info_matches) == 0:
            raise Exception("No leave detail found")

        # 取得請假訊息，若無則為 None
        message = None
        if leave_data.has_message:
            # 0.日期 1.審核者姓名 2.來談內容 3.是否為不准假(目前用意不明)
            # 請假訊息格式 be like leave_message[leave_message.length] = new Array("2023/09/30","審核者","審核原因","");
            message_pattern = r'leave_message\[[^\]]+\] = new Array\("([^"]*)","([^"]*)","([^"]*)","([^"]*)"\)'
            # 取得請假訊息 matches，內容為 tuple，會包含 日期、審核者、審核原因。
            message_matches = re.findall(message_pattern, res.text)
            # 若無請假訊息，則 raise exception
            if len(message_matches) == 0:
                raise Exception("No message found")
            # 取得請假訊息
            message = message_matches[1][2]

        # 設定請假詳細資訊，因為請假基本單位為每節課，因此可能有多筆請假詳細資訊
        leave_details = [
            LeaveDetail(
                course_name=i[2], # 課程名稱
                status=i[5], # 審核狀態
                status_description=i[9], # 審核狀態說明
                period=i[1], # 課程代號
                reviewer_name=i[3], # 審核人
                reviewer_relationship=i[4], # 審核人與課程的關係
                message=message, # 請假訊息
                meeting_name=i[7] if i[7] else None, # 集會名稱
                dorm_meeting_name=i[8] if i[8] else None, # 宿舍重要集會名稱
            )
            for i in info_matches
        ]
        # 設定請假詳細資訊
        leave_data.set_details(leave_details)
        return leave_data

    @staticmethod
    @login_required
    # 取得請假紀錄
    def list(
            conn : Connection,
            s_d : date = None,
            e_d : date = None
    ) -> list[LeaveData]:
        """
        取得請假紀錄
        :param conn: Connection
        :param s_d: 起始日期
        :param e_d: 結束日期
        :return: List[LeaveData]
        """

        def get_para(d1 : date = s_d, d2 : date = e_d):
            """
            取得查詢參數
            :param d1: 起始日期
            :param d2: 結束日期
            :return: 參數字串
            """

            # 若起始日期或結束日期為 None，則回傳空字串，表示不設定日期範圍
            if d1 is None or d2 is None:
                return ""
            # 回傳日期範圍參數，格式為 &sdate=2021-09-01&edate=2021-09-30
            return f"&sdate={d1.strftime('%Y-%m-%d')}&edate={d2.strftime('%Y-%m-%d')}"

        # 取得請假紀錄，並設定 PHP session id，用於驗證身分
        res = requests.get(
            f"https://sis.dyu.edu.tw/page_system.php?page=MTI={get_para(s_d, e_d)}",
            cookies={"PHPSESSID": conn.php_session_id}
        )

        # Response 轉碼成 utf-8
        res.encoding = "utf-8"

        # 請假紀錄格式 be like new Array("請假編號", "請假類別", "請假種類", "理由", "請假狀態", "是否有訊息", "日期", "證明文件連結");
        pattern = r'new Array\("([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)",([^,]*),"([^"]*)",[^,]*,"([^"]*)"\);'
        # 取得請假紀錄 matches，內容為 tuple，會包含 請假編號、請假類別、請假種類、理由、請假狀態、是否有訊息、日期、證明文件連結。
        matches = re.findall(pattern, res.text)

        # 若無請假紀錄，則回傳空 list
        if len(matches) == 0:
            return []
        
        return LeaveData.from_source(matches, conn.student_id)

    @staticmethod
    def info(
            s_time : date = date.today(),
            e_time : date = date.today(),
            s_id : str = None
    ) -> List[CourseWithDate]:
        """
        取得 指定時間、學號 的課程資訊(含請假資訊)
        :param s_time: 查詢 start time
        :param e_time: 查詢 end time
        :param s_id: 查詢學號
        :return: List[CourseWithDate]
        """

        if s_id is None:
            raise Exception("Student ID can not be None")

        # 取得課程資訊(含請假資訊)的 url
        url = DyuWebAPI.get_course_info_url(s_time, e_time, s_id)

        # 取得課程資訊(含請假資訊)，此連結無須登入即可取得，因此不需要傳入 PHP session id
        res = requests.get(url)

        # 若取得課程資訊(含請假資訊)失敗，則 raise exception
        if res.status_code < 200 or res.status_code >= 300:
            raise Exception(f"Get course info failed, status code: {res.status_code}")

        # Response 轉碼成 utf-8
        res.encoding = "utf-8"

        content = res.text

        # response 若為空字串，則回傳空 list，表此人當天無課程或查無此人
        if content == "":
            return []
        # 課程資訊(含請假資訊)格式 be like {日期},{課程代號},{課程名稱},{星期幾},{節測},{教師代號},{教師名稱},{請假狀態}; 以 ; 分隔每筆資料，在此去除空白字串
        periods = [a.strip() for a in content.split(';') if a]

        if len(periods) == 0:
            return []

        # 設定課程資訊(含請假資訊)，因為請假基本單位為每節課，因此可能有多筆課程資訊(含請假資訊)
        leave_status_list = [
            CourseWithDate(
                course_date=datetime.strptime(period[0], "%Y/%m/%d").date(), # 轉換日期格式
                course_weekday=int(period[3]), # 星期幾
                course_pending=period[7] != "0",  # 0 代表沒有送出請假
                course_id=period[1],
                course_period=int(period[4]),
                course_name=period[2],
                course_teacher=Teacher(
                    teacher_id=period[5],
                    teacher_name=period[6]
                )
            )
            for period in (p.split(',') for p in periods)
        ]

        return leave_status_list