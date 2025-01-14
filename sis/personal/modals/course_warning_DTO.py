class CourseWarningDTO:
    """
    課程警告資訊
    """
    def __init__(
            self,
            course_id: str,
            course_name: str,
            is_required: bool,
            teacher_name: str,
            is_warning: bool,
            warning_message: str,
            credit: int,
            comment: str
    ):
        """
        課程警告資訊
        :param course_id: 課程編號
        :param course_name: 課程名稱
        :param is_required: 是否必修
        :param teacher_name: 教師姓名
        :param is_warning: 是否有警告
        :param warning_message: 警告訊息
        :param credit: 學分數
        :param comment: 備註
        """
        self.course_id = course_id
        self.course_name = course_name
        self.is_required = is_required
        self.teacher_name = teacher_name
        self.is_warning = is_warning
        self.warning_message = warning_message
        self.credit = credit
        self.comment = comment

    @staticmethod
    def from_source(
            course_id: str,
            course_name: str,
            is_required: str,
            teacher_name: str,
            warning_message: str,
            credit: str,
            comment: str
    ):
        """
        將爬取的資料轉換成 CourseWarningDTO
        :param course_id: 課程編號
        :param course_name: 課程名稱
        :param is_required: 是否必修
        :param teacher_name: 教師姓名
        :param warning_message: 警告訊息
        :param credit: 學分數
        :param comment: 備註
        """
        return CourseWarningDTO(
            course_id,
            course_name,
            is_required == "必" or is_required == "必修",
            teacher_name,
            warning_message != "--",
            warning_message,
            int(credit),
            comment
        )

    def __repr__(self):
        return f"CourseWarningDTO(course_id={self.course_id}, course_name={self.course_name}, is_required={self.is_required}, teacher_name={self.teacher_name}, is_warning={self.is_warning}, warning_message={self.warning_message}, credit={self.credit}, comment={self.comment})"

    def __str__(self):
        return f"CourseWarningDTO(course_id={self.course_id}, course_name={self.course_name}, is_required={self.is_required}, teacher_name={self.teacher_name}, is_warning={self.is_warning}, warning_message={self.warning_message}, credit={self.credit}, comment={self.comment})"