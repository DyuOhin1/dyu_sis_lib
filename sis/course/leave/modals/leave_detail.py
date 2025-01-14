
class LeaveDetail:
    """
    請假詳細資訊，用於表示請假的詳細資訊，例如：課程名稱、審核狀態、審核者、審核者關係、訊息等等
    """
    def __init__(
            self,
            course_name : str,
            status : str,
            status_description : str,
            period: int,
            reviewer_name: str,
            reviewer_relationship : str,
            message : str = None,
            meeting_name : str = None,
            dorm_meeting_name : str = None,
    ):
        """
        :param course_name: 課程名稱
        :param status: 審核狀態
        :param status_description: 審核狀態描述
        :param period: 節次
        :param reviewer_name: 審核者姓名
        :param reviewer_relationship: 審核者關係，這裡的關係是指審核者與這堂課的審核關係，例如：任課老師、班導、系主任
        :param message: 訊息
        :param meeting_name: 會議名稱
        :param dorm_meeting_name: 宿舍會議名稱
        """
        self.course_name = course_name
        self.status = status
        self.status_description = status_description
        self.period = period
        self.reviewer_name = reviewer_name
        self.reviewer_relationship = reviewer_relationship
        self.message = message
        self.meeting_name = meeting_name
        self.dorm_meeting_name = dorm_meeting_name

    def __repr__(self):
        return f"LeaveDetail(course_name={self.course_name}, status={self.status}, status_description={self.status_description}, period={self.period}, reviewer_name={self.reviewer_name}, reviewer_relationship={self.reviewer_relationship}, message={self.message}, meeting_name={self.meeting_name}, dorm_meeting_name={self.dorm_meeting_name})"

    def __str__(self):
        return f"LeaveDetail(course_name={self.course_name}, status={self.status}, status_description={self.status_description}, period={self.period}, reviewer_name={self.reviewer_name}, reviewer_relationship={self.reviewer_relationship}, message={self.message}, meeting_name={self.meeting_name}, dorm_meeting_name={self.dorm_meeting_name})"