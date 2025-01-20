from sis.personal.modals.graduation.graduation_certification import GraduationCertification


class ComputerGraduation(GraduationCertification):
    """
    computer class - `ComputerGraduation`
    1. cert_id - 證照編號
    2. issuer - 核發單位/機關
    3. cert_date - 證號核發日期
    """
    def __init__(
            self, id: str,
            year: str,
            semester: str,
            title: str,
            cert_id : str,
            issuer : str,
            cert_date : str
    ):
        super().__init__(id, year, semester, title)
        self._cert_id = cert_id
        self._issuer = issuer
        self._cert_date = cert_date

    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "semester": self.semester,
            "title": self.title,
            "cert_id": self.cert_id,
            "issuer": self.issuer,
            "cert_date": self.cert_date
        }

    @property
    def cert_id(self):
        return self._cert_id

    @property
    def issuer(self):
        return self._issuer

    @property
    def cert_date(self):
        return self._cert_date

    def __str__(self):
        return f"ComputerGraduation(id={self.id}, year={self.year}, semester={self.semester}, title={self.title}, cert_id={self.cert_id}, issuer={self.issuer}, cert_date={self.cert_date})"

    def __repr__(self):
        return f"ComputerGraduation(id={self.id}, year={self.year}, semester={self.semester}, title={self.title}, cert_id={self.cert_id}, issuer={self.issuer}, cert_date={self.cert_date})"