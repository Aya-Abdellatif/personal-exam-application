from question import Question
from data_manager import DataManager
import random


class ExamMaker:
    @staticmethod
    def make_exam(topics: list[tuple[str, int]]) -> list[Question]:
        all_questions: dict[str, list[Question]] = DataManager.get_all_questions()
        questions = []

        # Add Biased Questions
        for topic, frequency in topics:
            topic_questions = all_questions[topic]

            for _ in range(frequency):
                chosen_question = random.choice(topic_questions)
                questions.append(chosen_question)
                topic_questions.remove(chosen_question)

        for _ in range(6):
            random_topic = random.choice(list(all_questions.keys()))
            random_question = random.choice(all_questions[random_topic])
            questions.append(random_question)
            all_questions[random_topic].remove(random_question)

        return questions

    @staticmethod
    def make_random_exam() -> list[Question]:
        all_questions: dict[str, list[Question]] = DataManager.get_all_questions()
        questions: list[Question] = []
        for topic in all_questions.keys():
            for _ in range(5):
                random_question = random.choice(all_questions[topic])
                questions.append(random_question)

                # Removing the question so that we don't use it again
                all_questions[topic].remove(random_question)

        return questions

    @staticmethod
    def get_exams(
        exam_count: int, filtered_frequent_itemsets: list[tuple[list[str], int]]
    ) -> list[list[Question]]:
        exams: list[list[Question]] = []

        one_itemsets = ExamMaker._get_n_itemsets(filtered_frequent_itemsets, 1)
        two_itemsets = ExamMaker._get_n_itemsets(filtered_frequent_itemsets, 2)

        # itemset[1] represents the frequency
        sorted_frequent_itemsets = dict(
            sorted(two_itemsets.items(), key=lambda itemset: itemset[1], reverse=True)
        )[:exam_count]

        for exam_topics, _ in sorted_frequent_itemsets.items():
            first_topic = exam_topics[0]
            second_topic = exam_topics[1]

            first_topic_frequency = one_itemsets[first_topic,]
            second_topic_frequency = one_itemsets[second_topic,]

            total_frequency = first_topic_frequency + second_topic_frequency

            first_topic_ratio = first_topic_frequency / total_frequency

            first_topic_question_count = round(14 * first_topic_ratio)
            second_topic_question_count = 14 - first_topic_question_count

            exams.append(
                ExamMaker.make_exam(
                    [
                        (first_topic, first_topic_question_count),
                        (second_topic, second_topic_question_count),
                    ]
                )
            )

        for _ in range(max(exam_count - len(sorted_frequent_itemsets), 0)):
            exams.append(ExamMaker.make_random_exam())

        return exams

    @staticmethod
    def _get_n_itemsets(
        filtered_frequent_itemsets: list[tuple[list[str], int]],
        n: int,
    ) -> dict[tuple[str, ...], int]:
        return {
            tuple(itemset): frequency
            for itemset, frequency in filtered_frequent_itemsets
            if len(itemset) == n
        }
