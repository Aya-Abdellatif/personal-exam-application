import unittest
from unittest.mock import patch, mock_open
import os
import pandas as pd
from data_manager import DataManager


class TestDataManager(unittest.TestCase):
    @patch("os.listdir")
    @patch("builtins.open", new_callable=mock_open, read_data="Topic : Math\nSubtopic : Algebra\n\nQ: What is 2+2?\na) 2\nb) 3\nc) 4\nd) 5\n\nAnswer: c\n")
    @patch("pandas.DataFrame.to_csv")
    def test_prepare_all(self, mock_to_csv, mock_open_file, mock_listdir):
        mock_listdir.return_value = ["test_file.txt"]

        DataManager.prepare_all()

        mock_open_file.assert_called_once_with(os.path.join(os.getcwd(), "Text Data", "test_file.txt"), "r")
        mock_to_csv.assert_called_once()

    @patch("os.listdir")
    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_merge_csv_files(self, mock_to_csv, mock_read_csv, mock_listdir):
        mock_listdir.return_value = ["file1.csv", "file2.csv"]
        mock_read_csv.side_effect = [
            pd.DataFrame({"topic": ["Math"], "questionText": ["What is 2+2?"], "answer": ["C"]}),
            pd.DataFrame({"topic": ["Science"], "questionText": ["What is H2O?"], "answer": ["A"]}),
        ]

        DataManager.merge_csv_files(os.getcwd())

        mock_to_csv.assert_called_once()

    @patch("pandas.read_csv")
    def test_load_and_sort_transactions(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            "Transaction": ["Math;Science", "Science;Math;Math;History"],
        })

        sorted_transactions = DataManager.load_and_sort_transactions()

        self.assertEqual(sorted_transactions, [["Math", "Science"], ["Math", "Math", "Science", "History"]])

    @patch("pandas.read_csv")
    def test_get_all_questions(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            "topic": ["Math", "Science"],
            "questionText": ["What is 2+2?", "What is H2O?"],
            "choiceA": ["2", "Water"],
            "choiceB": ["3", "Oxygen"],
            "choiceC": ["4", "Hydrogen"],
            "choiceD": ["5", "Carbon"],
            "answer": ["C", "A"],
        })

        all_questions = DataManager.get_all_questions()

        self.assertIn("Math", all_questions)
        self.assertIn("Science", all_questions)
        self.assertEqual(len(all_questions["Math"]), 1)
        self.assertEqual(len(all_questions["Science"]), 1)

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_append_transaction(self, mock_to_csv, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({"Transaction": ["Math;Science"]})

        DataManager.append_transaction(["History", "Art"])

        mock_to_csv.assert_called_once()

    @patch("pandas.read_csv")
    def test_get_average_score(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            "Transaction": [
                "Math;Science",
                "Math;Science;History;Art"
            ],
        })

        average_score = DataManager.get_average_score()

        self.assertAlmostEqual(average_score, 17.0)


if __name__ == "__main__":
    unittest.main()
