class GraduationCertification:
    """
    base class - GraduationCertification
    1. id - 序號
    2. year - 學年
    3. semester - 學期
    4. title - 認證標題名稱
    """
    def __init__(
            self,
            id : str,
            year : str,
            semester : str,
            title : str
    ):
        self._id = id
        self._year = year
        self._semester = semester
        self._title = title

    @property
    def id(self):
        return self._id

    @property
    def year(self):
        return self._year

    @property
    def semester(self):
        return self._semester

    @property
    def title(self):
        return self._title

    def __str__(self):
        return f"GraduationCertification(id={self.id}, year={self.year}, semester={self.semester}, title={self.title})"

    def __repr__(self):
        return f"GraduationCertification(id={self.id}, year={self.year}, semester={self.semester}, title={self.title})"