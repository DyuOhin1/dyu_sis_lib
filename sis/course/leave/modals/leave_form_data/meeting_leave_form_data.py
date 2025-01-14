from datetime import date
from typing import Optional, BinaryIO

from sis.constant.api import DyuWebAPI
from sis.course.leave.constant.departments import Department
from sis.course.leave.constant.leave_type import LeaveType, MeetingType
from sis.course.leave.modals.leave_form_data.leave_form_data import LeaveFormData


class MeetingLeaveFormData(LeaveFormData):
    """
    重要集會請假 FormData
    """
    def __init__(
            self,
            start_date: date,
            leave_type: LeaveType,
            meeting_type: MeetingType,
            meeting_name : str,
            smye: int,
            smty: int,
            reason: str,
            from_dept: Optional[Department] = None,
            file: Optional[BinaryIO] = None
    ):
        """
        重要集會請假 FormData
        :param start_date: 請假日期
        :param leave_type: 請假種類
        :param meeting_type: 集會類型
        :param meeting_name: 集會名稱
        :param smye: 集會年度
        :param smty: 集會期別
        :param reason: 理由
        :param from_dept: 派出單位
        :param file: 證明文件
        """
        super().__init__(start_date, leave_type, reason, from_dept, file)
        self.meeting_type = meeting_type
        self.meeting_name = meeting_name
        self.smye = smye
        self.smty = smty
        self.request_url = DyuWebAPI.SIS_MEETING_LEAVE_POST

    def __str__(self):
        return f"MeetingLeaveFormData(start_date={self.start_date}, type={self.leave_type}, meeting_type={self.meeting_type}, meeting={self.meeting}, smye={self.smye}, smty={self.smty}, from_dept={self.from_dept}, file={self.file}, reason={self.reason})"

    def to_form_data(self) -> dict:
        """
        覆寫並使用父類別的 to_form_data 方法並加入集會相關資訊
        :return: 格式化後的 data
        """
        super_data = super().to_form_data()
        super_data["data"]["metting_type"] = self.meeting_type.code
        super_data["data"]["meeting"] = self.meeting_name
        super_data["data"]["smye"] = self.smye
        super_data["data"]["smty"] = self.smty

        return super_data