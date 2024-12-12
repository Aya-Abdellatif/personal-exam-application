import pandas as pd
import os

class DataManager:
    @staticmethod
    def prepare_all(file_directory: str):
        for filename in os.listdir(os.path.join(os.getcwd(), file_directory)):
            DataManager.prepare(os.path.join(file_directory, filename), "CSV Data/")
        print("OK")

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
                correct_answer = lines[current_index + 7][-2] if lines[current_index + 7][-1] == '\n' else lines[current_index + 7][-1] 

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
        df.to_csv(os.path.join(output_directory, f"{topic}-{subtopic}.csv"), index=False)

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
    ):

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
        merged_df.to_csv('all_data.csv', index=False)
