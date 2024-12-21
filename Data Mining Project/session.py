from typing import Optional

from exam_maker import Question


class Session:
    """
    A class that represents the session variables.
    """

    submitted_exam: bool = False
    exam_index: Optional[int] = None
    exam_answers: dict[int, Optional[str]] = {i: None for i in range(20)}
    exam: Optional[list[Question]] = None

    def __init__(self):
        self.submitted_exam = Session.submitted_exam
        self.exam_index = Session.exam_index
        self.exam_answers = Session.exam_answers
        self.exam = Session.exam

    @staticmethod
    def reset():
        """
        Resets the session variables to the default values.
        """
        Session.submitted_exam = False
        Session.exam_index = None
        Session.exam_answers = {i: None for i in range(20)}
        Session.exam = None
