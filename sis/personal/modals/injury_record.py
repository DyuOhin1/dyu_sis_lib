from datetime import datetime


class InjuryRecord:
    def __init__(
            self,
            semester: str,
            record_time: datetime,
            is_on_campus: bool,
            event_type: str,
            location: str,
            injured_part: str,
            follow_up: str,
            comment: str = None,
    ):
        """
        受傷紀錄
        :param semester: 學年學期
        :param record_time: 紀錄時間
        :param is_on_campus: 是否在校
        :param event_type: 事件類型
        :param location: 事件地點
        :param injured_part: 受傷部位
        :param follow_up: 後續處理
        :param comment: 備註
        """
        self.semester = semester
        self.record_time = record_time
        self.is_on_campus = is_on_campus
        self.event_type = event_type
        self.location = location
        self.injured_part = injured_part
        self.follow_up = follow_up
        self.comment = comment

    def __str__(self):
        return f"InjuryRecord(semester={self.semester}, record_time={self.record_time}, is_on_campus={self.is_on_campus}, event_type={self.event_type}, location={self.location}, injured_part={self.injured_part}, follow_up={self.follow_up}, comment={self.comment})"

    def __repr__(self):
        return f"InjuryRecord(semester={self.semester}, record_time={self.record_time}, is_on_campus={self.is_on_campus}, event_type={self.event_type}, location={self.location}, injured_part={self.injured_part}, follow_up={self.follow_up}, comment={self.comment})"

    @staticmethod
    def from_source(
            semester: str,
            record_time: str,
            is_on_campus: str,
            event_type: str,
            location: str,
            injured_part: str,
            follow_up: str,
            comment: str,
    ):
        """
        將爬取的資料轉換成 InjuryRecord
        :param semester: 學年學期
        :param record_time: 紀錄時間
        :param is_on_campus: 是否在校
        :param event_type: 事件類型
        :param location: 事件地點
        :param injured_part: 受傷部位
        :param follow_up: 後續處理
        :param comment: 備註
        :return: InjuryRecord
        """
        return InjuryRecord(
            semester,
            datetime.strptime(record_time, "%Y/%m/%d %H:%M"),
            is_on_campus == "校內",
            event_type,
            location,
            injured_part,
            follow_up,
            None if comment == "n.a." else comment
        )