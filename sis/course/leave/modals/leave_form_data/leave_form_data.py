from datetime import date
from typing import Optional, BinaryIO

from sis.course.leave.constant.departments import Department
from sis.course.leave.constant.leave_type import LeaveType


class LeaveFormData:
    """
    所有請假請求的基本格式
    包含：請假開始日期、請假種類、理由、派出單位(公假專用)、證明文件
    """ 
    def __init__(
            self,
            start_date: date,
            leave_type: LeaveType,
            reason: str,
            from_dept: Department = None,
            file: BinaryIO = None
    ):
        """
        請假 FormData
        :param start_date: 請假日期
        :param leave_type: 請假種類
        :param reason: 理由
        :param from_dept: 派出單位
        :param file: 證明文件
        """

        self.day = 1
        self.start_date = start_date
        self.leave_type = leave_type
        self.reason = reason
        self.max_file_size = 2097152
        self.from_dept = from_dept
        self.file = file
        self.request_url = None

    def __str__(self):
        return f"LeaveFormDate(start_date={self.start_date}, type={self.leave_type}, from_dept={self.from_dept}, file={self.file}, reason={self.reason})"

    def to_form_data(self) -> dict:
        """
        格式化成請假系統需要的格式
        :return: 格式化後的 data
        """

        if self.leave_type == LeaveType.OFFICIAL and not self.from_dept:
            raise ValueError("公假必須有要有派出單位")

        # 格式化成請假系統需要的格式
        return {
            "data": {
                "StartDate": self.start_date.strftime("%Y/%m/%d"),
                "cla": self.leave_type.code,  # 請假類型
                "dept": self.from_dept.code if self.from_dept else "",  # 公假必須有要有派出單位
                "MAX_FILE_SIZE": self.max_file_size,  # 2MB
                "reas": self.reason,
                "day": 1,
            },
            "file": {'path': self.file}
        }