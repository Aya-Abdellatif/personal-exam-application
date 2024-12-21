import unittest
from unittest.mock import patch
from exam_maker import ExamMaker
from question import Question


class TestExamMaker(unittest.TestCase):
    @patch("exam_maker.DataManager.get_all_questions")
    def test_make_exam(self, mock_get_all_questions):
        mock_questions = {
            "Math": [
                Question(
                    question_text=f"Math Q{i}",
                    topic="Math",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="A",
                )
                for i in range(20)
            ],
            "Science": [
                Question(
                    question_text=f"Science Q{i}",
                    topic="Science",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="B",
                )
                for i in range(20)
            ],
        }
        mock_get_all_questions.return_value = mock_questions

        topics = [("Math", 8), ("Science", 6)]
        exam = ExamMaker.make_exam(topics)

        self.assertEqual(len(exam), 20)
        self.assertGreaterEqual(len([q for q in exam if q.topic == "Math"]), 8)
        self.assertGreaterEqual(len([q for q in exam if q.topic == "Science"]), 6)
        self.assertEqual(len(set(exam)), 20, "Questions should be unique.")

    @patch("exam_maker.DataManager.get_all_questions")
    def test_make_random_exam(self, mock_get_all_questions):
        mock_questions = {
            "Math": [
                Question(
                    question_text=f"Math Q{i}",
                    topic="Math",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="A",
                )
                for i in range(5)
            ],
            "Science": [
                Question(
                    question_text=f"Science Q{i}",
                    topic="Science",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="B",
                )
                for i in range(5)
            ],
            "History": [
                Question(
                    question_text=f"History Q{i}",
                    topic="History",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="C",
                )
                for i in range(5)
            ],
            "Art": [
                Question(
                    question_text=f"Art Q{i}",
                    topic="Art",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="D",
                )
                for i in range(5)
            ],
        }
        mock_get_all_questions.return_value = mock_questions

        exam = ExamMaker.make_random_exam()

        self.assertEqual(len(exam), 20)
        for topic in mock_questions.keys():
            self.assertEqual(len([q for q in exam if q.topic == topic]), 5)
        self.assertEqual(len(set(exam)), 20, "Questions should be unique.")

    @patch("exam_maker.DataManager.get_all_questions")
    def test_get_exams(self, mock_get_all_questions):
        mock_questions = {
            "Math": [
                Question(
                    question_text=f"Math Q{i}",
                    topic="Math",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="A",
                )
                for i in range(20)
            ],
            "Science": [
                Question(
                    question_text=f"Science Q{i}",
                    topic="Science",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="B",
                )
                for i in range(20)
            ],
            "Arts": [
                Question(
                    question_text=f"Arts Q{i}",
                    topic="Arts",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="A",
                )
                for i in range(20)
            ],
            "History": [
                Question(
                    question_text=f"History Q{i}",
                    topic="History",
                    choice_a="A",
                    choice_b="B",
                    choice_c="C",
                    choice_d="D",
                    answer="A",
                )
                for i in range(20)
            ],
        }
        mock_get_all_questions.return_value = mock_questions

        filtered_frequent_itemsets = [
            (["Math", "Science"], 10),
            (["Math"], 5),
            (["Science"], 5),
        ]

        exams = ExamMaker.get_exams(2, filtered_frequent_itemsets)

        self.assertEqual(len(exams), 2)
        for exam in exams:
            self.assertEqual(len(exam), 20)
            self.assertEqual(len(set(exam)), 20, "Questions should be unique.")

    def test_get_n_itemsets(self):
        frequent_itemsets = [
            (["Math"], 5),
            (["Science"], 3),
            (["Math", "Science"], 7),
            (["Art", "History"], 4),
        ]

        one_itemsets = ExamMaker._get_n_itemsets(frequent_itemsets, 1)
        two_itemsets = ExamMaker._get_n_itemsets(frequent_itemsets, 2)

        self.assertEqual(one_itemsets, {("Math",): 5, ("Science",): 3})
        self.assertEqual(two_itemsets, {("Math", "Science"): 7, ("Art", "History"): 4})


if __name__ == "__main__":
    unittest.main()
