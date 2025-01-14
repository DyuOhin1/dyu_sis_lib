from datetime import date, timedelta
from typing import Optional, BinaryIO

from sis.constant.api import DyuWebAPI
from sis.course.leave.constant.departments import Department
from sis.course.leave.constant.leave_type import LeaveType
from sis.modals.course import CourseWithDate
from sis.course.leave.modals.leave_form_data.leave_form_data import LeaveFormData


class CourseLeaveFormData(LeaveFormData):
    """
    上課請假 FormData
    """
    def __init__(
            self,
            course: list[CourseWithDate],
            leave_type: LeaveType,
            reason: str,
            start_date: date = None,
            end_date: date = None,
            from_dept: Optional[Department] = None,
            file: Optional[BinaryIO] = None
    ):
        """
        上課請假 FormData
        :param start_date: 請假日期
        :param end_date: 結束日期
        :param course: 課程資訊
        :param leave_type: 請假種類
        :param reason: 理由
        :param from_dept: 派出單位
        :param file: 證明文件
        """

        super().__init__(start_date, leave_type, reason, from_dept, file)
        self.end_date = end_date
        self.course = course
        self.request_url = DyuWebAPI.SIS_LEAVE_POST
        self.setup_date_range()

    def setup_date_range(self):
        """
        取得日期為最前面做為開始日期，最後面做為結束日期
        """
        self.start_date = min(i.course_date for i in self.course)
        self.end_date = max(i.course_date for i in self.course)

    def __str__(self):
        return f"CourseLeaveFormData(start_date={self.start_date}, end_date={self.end_date}, course={self.course}, type={self.leave_type}, from_dept={self.from_dept}, file={self.file}, reason={self.reason})"

    def to_form_data(self) -> dict:
        """
        覆寫並使用父類別的 to_form_data 方法並加入課程相關資訊
        :return: 格式化後的 data
        """
        if self.course is None == 0:
            raise ValueError("Course must be provided")
        if self.end_date < self.start_date:
            raise ValueError("End date must be later than start date")

        def get_seq(course: list[CourseWithDate]) -> list[str]:
            """
            因為請假系統需要的格式為 "2021/09/01,1,1"，所以要將課程資訊轉換成這樣的格式
            """
            return list(f"{i.course_date},{i.course_id},{i.course_period}" for i in course)

        super_data = super().to_form_data()
        super_data["data"]["EndDate"] = self.end_date.strftime("%Y/%m/%d")
        super_data["data"]["seq[]"] = get_seq(self.course)
        super_data["data"]["day"] = (self.end_date - self.start_date + timedelta(days=1)).days

        return super_data