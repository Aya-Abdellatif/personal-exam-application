from dataclasses import dataclass


@dataclass
class Question:
    question_text: str
    topic: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    answer: str
