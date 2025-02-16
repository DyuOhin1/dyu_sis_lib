from datetime import date
from typing import Generator

from sis.course.leave.modals.leave_detail import LeaveDetail
from datetime import datetime

class LeaveData:

    def __init__(
            self,
            id : str,
            category : str,
            leave_type : str,
            reason : str,
            leave_status : str,
            has_message : bool,
            date : date,
            document_link : str,
            details : list[LeaveDetail] = None
    ):
        """
        與 LeaveFormData 不同的是，這個是從網頁上爬取的資料
        :param id: 請假編號
        :param category: 請假類別
        :param leave_type: 請假種類
        :param reason: 理由
        :param leave_status: 請假狀態
        :param has_message: 是否有訊息
        :param date: 日期
        :param document_link: 證明文件連結
        """
        self.id = id
        self.category = category
        self.leave_type = leave_type
        self.reason = reason
        self.leave_status = leave_status
        self.has_message = has_message
        self.date = date
        self.document_link = document_link
        self.details = details

    def __str__(self):
        return f"LeaveData(id={self.id}, category={self.category}, leave_type={self.leave_type}, reason={self.reason}, leave_status={self.leave_status}, has_message={self.has_message}, date={self.date}, document_link={self.document_link}, details={self.details})"

    def __repr__(self):
        return f"LeaveData(id={self.id}, category={self.category}, leave_type={self.leave_type}, reason={self.reason}, leave_status={self.leave_status}, has_message={self.has_message}, date={self.date}, document_link={self.document_link}, details={self.details})"

    def set_details(self, details : Generator[LeaveDetail, None, None]):
        """
        設定請假詳細資訊
        :param details: 請假詳細資訊
        """
        self.details = details

    @staticmethod
    def from_source(matches : list, doc_link : str, student_id : str) -> list:
        """
        將爬取的資料轉換成 LeaveData
        :param matches: 爬取的資料
        :param student_id: 學生編號
        :return: LeaveData
        """
        return [
            LeaveData(
                id = match[0],
                category = match[1],
                leave_type = match[2],
                reason = match[3],
                leave_status = match[4],
                has_message = match[5] == "1",
                date = datetime.strptime(match[7], "%Y/%m/%d").date(),
                document_link = f'{doc_link}{student_id}/{match[8]}' if match[8] else None
            ) for match in matches
        ]