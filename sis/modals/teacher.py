class Teacher:
    def __init__(
            self,
            teacher_id: str,
            teacher_name: str,
    ):
        """
        教師類別
        :param teacher_id: 教師編號
        :param teacher_name: 教師姓名
        """

        self.teacher_id = teacher_id
        self.teacher_name = teacher_name

    def __str__(self):
        return f"Teacher(teacher_id={self.teacher_id}, teacher_name={self.teacher_name})"
    def __repr__(self):
        return f"Teacher(teacher_id={self.teacher_id}, teacher_name={self.teacher_name})"