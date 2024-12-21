from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    """
    A dataclass representing a question including all of its attributes.
    """

    question_text: str
    topic: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    answer: str
