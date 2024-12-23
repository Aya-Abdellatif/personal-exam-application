from typing import Optional

import pandas as pd
import os
from collections import Counter
from question import Question


TEXT_DATA_DIRECTORY_PATH = os.path.join(os.getcwd(), "Text Data")
CSV_DATA_DIRECTORY_PATH = os.path.join(os.getcwd(), "CSV Data")
TRANSACTIONS_DATA_PATH = os.path.join(os.getcwd(), "transactions.csv")


class DataManager:
    """
    A static class for managing everything related to data.
    """

    @staticmethod
    def prepare_all() -> None:
        """
        Converts all the text data to separate csv files.
        """
        for filename in os.listdir(TEXT_DATA_DIRECTORY_PATH):
            DataManager.prepare(os.path.join(TEXT_DATA_DIRECTORY_PATH, filename))
        print("PREPARING CSV FILES: OK")

    @staticmethod
    def prepare(filename: str) -> None:
        """
        Converts a single text file to a csv file
        :param filename: the filename to convert
        """
        questions = {
            "topic": [],
            "subTopic": [],
            "questionText": [],
            "choiceA": [],
            "choiceB": [],
            "choiceC": [],
            "choiceD": [],
            "answer": [],
        }

        with open(filename, "r") as file:
            lines = file.readlines()
            # print(*lines, sep='\n')
            # Remove first 8 characters to get the topic
            topic = lines[0][8:].replace("\n", "")
            subtopic = lines[1][11:].replace("\n", "")

            current_index = 2
            while current_index < len(lines):
                question_text = lines[current_index + 1][3:].replace("\n", "")
                choice_a = lines[current_index + 2][3:].replace("\n", "")
                choice_b = lines[current_index + 3][3:].replace("\n", "")
                choice_c = lines[current_index + 4][3:].replace("\n", "")
                choice_d = lines[current_index + 5][3:].replace("\n", "")
                correct_answer = (
                    lines[current_index + 7][-2]
                    if lines[current_index + 7][-1] == "\n"
                    else lines[current_index + 7][-1]
                )

                # Save question in dictionary
                DataManager._add_question(
                    questions,
                    topic,
                    subtopic,
                    question_text,
                    choice_a,
                    choice_b,
                    choice_c,
                    choice_d,
                    correct_answer,
                )

                # Move to the next question
                current_index += 8

        df = pd.DataFrame(questions)
        df.to_csv(
            os.path.join(CSV_DATA_DIRECTORY_PATH, f"{topic}-{subtopic}.csv"),
            index=False,
        )

    @staticmethod
    def _add_question(
        questions: dict[str, list[str]],
        topic: str,
        sub_topic: str,
        question_text: str,
        choice_a: str,
        choice_b: str,
        choice_c: str,
        choice_d: str,
        correct_answer: str,
    ) -> None:
        """
        Adds a question to the questions' dictionary.
        :param questions: the dictionary to add question to.
        :param topic: the topic of the question.
        :param sub_topic: the sub-topic of the question.
        :param question_text: the question text of the question.
        :param choice_a: choice_a of the question.
        :param choice_b: choice_b of the question.
        :param choice_c: choice_c of the question.
        :param choice_d: choice_d of the question.
        :param correct_answer: the correct answer in the form of a/b/c/d.
        """
        questions["topic"].append(topic)
        questions["subTopic"].append(sub_topic)
        questions["questionText"].append(question_text)
        questions["choiceA"].append(choice_a)
        questions["choiceB"].append(choice_b)
        questions["choiceC"].append(choice_c)
        questions["choiceD"].append(choice_d)
        questions["answer"].append(correct_answer)

    @staticmethod
    def merge_csv_files(file_directory: str) -> None:
        """
        Merges all csv files into a single csv file.
        :param file_directory: the directory containing all the csv files.
        """
        dataframes = []

        # Loop through all files in the directory
        for filename in os.listdir(file_directory):
            filepath = os.path.join(file_directory, filename)
            df = pd.read_csv(filepath)
            dataframes.append(df)

        # Merge all dataframes
        merged_df = pd.concat(dataframes, ignore_index=True)

        # Save the merged dataframe to a new CSV file
        merged_df.to_csv("all_data.csv", index=False)

    @staticmethod
    def load_and_sort_transactions() -> pd.DataFrame:
        """
        Loads and sorts the transactions csv files into a pandas dataframe.
        :return: a dataframe containing all the sorted transactions
        """
        # Read the CSV file
        df = pd.read_csv(os.path.join(os.getcwd(), "transactions.csv"))

        # Convert transactions back to lists
        df["Transaction"] = df["Transaction"].apply(lambda x: x.split(";"))

        # Count global frequencies of topics
        flat_transactions = [item for sublist in df["Transaction"] for item in sublist]
        item_counts = Counter(flat_transactions)

        # Sort transactions based on item frequencies
        def sort_transaction(transaction):
            return sorted(transaction, key=lambda x: (-item_counts[x], x))

        df["Sorted Transaction"] = df["Transaction"].apply(sort_transaction)

        return df["Sorted Transaction"].tolist()

    @staticmethod
    def get_all_questions() -> dict[str, list[Question]]:
        """
        returns all the questions in the dataset
        :return: a dictionary containing all the topics mapped to all a list of questions for each topic.
        """
        df = pd.read_csv(os.path.join(os.getcwd(), "all_data.csv"))
        all_questions: dict[str, list[Question]] = {}
        for _, row in df.iterrows():
            if row["topic"] not in all_questions:
                all_questions[row["topic"]] = []
            question: Question = Question(
                question_text=row["questionText"],
                topic=row["topic"],
                choice_a=row["choiceA"],
                choice_b=row["choiceB"],
                choice_c=row["choiceC"],
                choice_d=row["choiceD"],
                answer=row["answer"],
            )
            all_questions[row["topic"]].append(question)
        return all_questions

    @staticmethod
    def append_transaction(transaction: list[str]) -> None:
        """
        Add a new transactions to the transactions csv file.
        :param transaction: the transaction as list of strings to add in the csv file.
        """
        df = pd.read_csv(TRANSACTIONS_DATA_PATH)
        df.loc[len(df)] = ";".join(transaction)
        df.to_csv(TRANSACTIONS_DATA_PATH, index=False)

    @staticmethod
    def get_average_score() -> Optional[float]:
        """
        Returns the average score of the transactions csv file.
        :return: the average score of the transactions csv file or none if there is no transactions.
        """
        df = pd.read_csv(TRANSACTIONS_DATA_PATH)
        exam_count = len(df["Transaction"])
        if exam_count == 0:
            return None
        # The number of wring answers in each row is equal to the number of semicolons in that row + 1
        # So we iterate over all the rows and count the number of (semicolons + 1)
        wrong_count = sum([row.count(";") + 1 for row in df["Transaction"].tolist()])

        correct_count = exam_count * 20 - wrong_count

        return round(correct_count / exam_count, 2)
