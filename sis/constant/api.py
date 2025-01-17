from datetime import date

class DyuWebAPI:
    # 學生資訊系統
    SIS_HOST = "https://sis.dyu.edu.tw/"
    # 登入
    SIS_LOGIN = SIS_HOST + "st_login.php"
    SIS_PERSONAL_COURSE_LIST = SIS_HOST + "course_list/pdf_cour_list.php"
    SIS_GRADUATION_INFO = SIS_HOST + "page_system.php?page=Mjk=&ready=1"
    SIS_GRADUATION_INFO_PDF = SIS_HOST + "graduation_info/stgrad_pdf_stno.php"

    # 綜合資料卡
    SIS_PERSONAL_INFO = SIS_HOST + "page_system.php?page=MQ=="
    # 請假頁面
    SIS_LEAVE = SIS_HOST + "page_system.php?page=MTI="
    # 指定學號課程資訊(含請假狀態)
    SIS_LEAVE_COURSE_INFO = SIS_HOST + "leave/student_class.php"
    # 請假 post url
    SIS_LEAVE_POST = SIS_HOST + "leave/leave_data.php"
    # 請假補交證明 post url
    SIS_LEAVE_SUBMIT_DOC = SIS_HOST + "leave/update_path.php"
    # 重要集會請假 post url
    SIS_MEETING_LEAVE_POST = SIS_HOST + "leave/meeting_leave_data.php"
    # 請假取消 url, doc_id 為請假紀錄的 id, page 為送出後　return 的頁面
    SIS_LEAVE_CANCEL = SIS_HOST + "leave/leave_cancel.php"
    # 請假紀錄詳細資訊, doc_id 為請假紀錄的 id
    SIS_LEAVE_DETAIL = SIS_HOST + "leave/leave_detail.php"
    # 受傷紀錄
    SIS_INJURY_RECORD = SIS_HOST + "page_system.php?page=NQ=="
    # 課程預警
    SIS_COURSE_WARNING = SIS_HOST + "page_system.php?page=OQ=="


    @staticmethod
    def get_course_info_url(s_date : date, e_date : date, s_id : str) -> str:
        """
        取得指定學號在指定日期區間的課程資訊(含請假狀態)
        :param s_date: 起始日期, 格式: YYYY/MM/DD
        :param e_date: 結束日期, 格式: YYYY/MM/DD
        :param s_id: 學號, 格式: 1英文+7數字
        :return: 格式：{日期},{課程代號},{課程名稱},{星期幾},{節測},{教師代號},{教師名稱},{請假狀態};
        """

        # 這邊的參數是用來組成 url 的 query string
        para = {
            "ls_sdt" : s_date.strftime("%Y/%m/%d"),
            "ls_edt" : e_date.strftime("%Y/%m/%d"),
            "stno" : s_id.upper()
        }

        # 將參數組成 query string, be like "ls_sdt=2021/09/01&ls_edt=2021/09/30&stno=A1234567"
        query_string = "&".join((f"{k}={v}" for k, v in para.items()))
        # 組成完整的 url
        url = f"{DyuWebAPI.SIS_LEAVE_COURSE_INFO}?{query_string}"
        return url