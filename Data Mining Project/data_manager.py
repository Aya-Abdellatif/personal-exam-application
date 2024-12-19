import pandas as pd
import os
from collections import Counter
from question import Question

class DataManager:
    @staticmethod
    def prepare_all(file_directory: str) -> None:
        for filename in os.listdir(os.path.join(os.getcwd(), file_directory)):
            DataManager.prepare(os.path.join(file_directory, filename), "CSV Data/")
        print("PREPARING CSV FILES: OK")

    @staticmethod
    def prepare(filename: str, output_directory: str = "/") -> None:
        print(filename)
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
            os.path.join(output_directory, f"{topic}-{subtopic}.csv"), index=False
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
    def load_and_sort_csv(file_path) -> pd.DataFrame:
        # Read the CSV file
        df = pd.read_csv(file_path)

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
        df = pd.read_csv(os.path.join(os.getcwd(), "all_data.csv"))
        all_questions: dict[str, list[Question]] = {}
        for _, row in df.iterrows():
            if row["topic"] not in all_questions:
                all_questions[row["topic"]] = []
            question : Question = Question(
                question_text=row["questionText"],
                topic=row["topic"],
                choice_a=row["choiceA"],
                choice_b=row["choiceB"],
                choice_c=row["choiceC"],
                choice_d=row["choiceD"],
                answer=row["answer"]
            )
            all_questions[row["topic"]].append(question)
            return all_questions
        
    @staticmethod
    def append_transaction(transaction: list[str]) -> None:
        df = pd.read_csv(os.path.join(os.getcwd(), "transactions.csv"))
        df.append(";".join(transaction))
        df.to_csv("transactions.csv", index=False)