from datetime import date
from sis.modals.teacher import Teacher


class Course:
    """
    開發階段 location 在 icloud，先塞 None
    """
    def __init__(
            self,
            course_id: str,
            course_period: int,
            course_name: str,
            course_teacher: Teacher,
            course_location: str = None,
    ):
        """
        課程類別
        :param course_id: 課程編號
        :param course_period: 課程節次
        :param course_name: 課程名稱
        :param course_teacher: 課程教師
        :param course_location: 課程地點
        """

        self.course_id = course_id
        self.course_period = course_period
        self.course_name = course_name
        self.course_teacher = course_teacher
        self.location = course_location

class CourseWithDate(Course):
    def __init__(
            self,
            course_date: date,
            course_weekday: int,
            course_pending: bool,
            course_id: str,
            course_period: int,
            course_name: str,
            course_teacher: Teacher,
            location: str = None,
    ):
        """
        課程類別(含日期、星期、請假狀態)
        :param course_date: 課程日期
        :param course_weekday: 課程星期
        :param course_pending: 課程是否有送出請假
        :param course_id: 課程編號
        :param course_period: 課程節次
        :param course_name: 課程名稱
        :param course_teacher: 課程教師
        :param location: 課程地點
        """
        super().__init__(course_id, course_period, course_name, course_teacher, location)
        self.course_date = course_date
        self.course_weekday = course_weekday
        self.course_pending = course_pending

    def __str__(self):
        return f"CourseWithDate(course_date={self.course_date}, course_weekday={self.course_weekday}, course_pending={self.course_pending}, course_id={self.course_id}, course_period={self.course_period}, course_name={self.course_name}, course_teacher={self.course_teacher}, location={self.location})"

    def __repr__(self):
        return f"CourseWithDate(course_date={self.course_date}, course_weekday={self.course_weekday}, course_pending={self.course_pending}, course_id={self.course_id}, course_period={self.course_period}, course_name={self.course_name}, course_teacher={self.course_teacher}, location={self.location})"