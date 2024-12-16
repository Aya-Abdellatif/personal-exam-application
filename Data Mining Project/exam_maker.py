from question import Question
from DataManager import DataManager
import random
class ExamMaker:
    @staticmethod
    def make_exam(topics: list[tuple[str, int]]) -> list[Question]:
        questions = []
        for topic, frequency in topics:
            topic_questions = DataManager.get_questions_with_topic(topic)

            for _ in range(frequency):
                chosen_question = random.choice(topic_questions)
                questions.append(Question(*chosen_question))
                topic_questions.remove(chosen_question)

        return questions
        
    def prepare_exams(exam_count: int, filtered_frequent_itemsets):
        ...