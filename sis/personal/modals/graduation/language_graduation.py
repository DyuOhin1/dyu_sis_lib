from sis.personal.modals.graduation.graduation_certification import GraduationCertification


class LanguageGraduation(GraduationCertification):
    """
    Chinese and English class - `LanguageGraduation`
    1. score - 成績/結果
    2. issuer - 核發單位/機關
    """
    def __init__(
            self, id: str,
            year: str,
            semester: str,
            title: str,
            score: str,
            issuer: str = None
    ):
        super().__init__(id, year, semester, title)
        self._score = score
        self._issuer = issuer

    @property
    def score(self):
        return self._score

    @property
    def issuer(self):
        return self._issuer

    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "semester": self.semester,
            "title": self.title,
            "score": self.score,
            "issuer": self.issuer
        }

    def __str__(self):
        return f"LanguageGraduation(id={self.id}, year={self.year}, semester={self.semester}, title={self.title}, score={self.score}, issuer={self.issuer})"

    def __repr__(self):
        return f"LanguageGraduation(id={self.id}, year={self.year}, semester={self.semester}, title={self.title}, score={self.score}, issuer={self.issuer})"