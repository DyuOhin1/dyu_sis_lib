class WorkingProject:
    """
    Working Project -

    1. id - item id
    2. max_hours -  最大採計時數
    3. total_hours - 累計時數
    4. cert_hours - 可認證時數
    5. title - 名稱
    """

    def __init__(
            self,
            id : str,
            max_hours : int,
            total_hours : int,
            cert_hours : int,
            title : str,
            detail_link : str
    ):
        self._id = id
        self._max_hours = max_hours
        self._total_hours = total_hours
        self._cert_hours = cert_hours
        self._title = title
        self._detail_link = detail_link

    @property
    def id(self):
        return self._id

    @property
    def max_hours(self):
        return self._max_hours

    @property
    def total_hours(self):
        return self._total_hours

    @property
    def cert_hours(self):
        return self._cert_hours

    @property
    def title(self):
        return self._title

    @property
    def detail_link(self):
        return self._detail_link

    def to_dict(self):
        return {
            "id": self.id,
            "max_hours": self.max_hours,
            "total_hours": self.total_hours,
            "cert_hours": self.cert_hours,
            "title": self.title,
            "detail_link": self.detail_link
        }

    def __str__(self):
        return f"WorkingProject(id={self.id}, max_hours={self.max_hours}, total_hours={self.total_hours}, cert_hours={self.cert_hours}, title={self.title})"

    def __repr__(self):
        return f"WorkingProject(id={self.id}, max_hours={self.max_hours}, total_hours={self.total_hours}, cert_hours={self.cert_hours}, title={self.title})"