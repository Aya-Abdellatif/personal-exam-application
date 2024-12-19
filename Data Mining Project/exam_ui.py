import streamlit as st
import base64

from question import Question

from data_manager import DataManager
from exam_maker import ExamMaker
from frequent_pattern_manager import FrequentPatternManager


def get_exams() -> list[list[Question]]:
    transactions = DataManager.load_and_sort_transactions()
    fp_tree = FrequentPatternManager.build_fp_tree(transactions)
    frequent_patterns = FrequentPatternManager.mine_fp_tree(fp_tree.header_table, 2)
    filtered_patterns = FrequentPatternManager.filter_items_with_duplicates(
        frequent_patterns
    )
    return ExamMaker.get_exams(3, filtered_patterns)


def check_answer(user_answer: str, correct_answer_char: str, question: Question):
    return user_answer == getattr(question, f"choice_{correct_answer_char}")


def add_background_image(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/png;base64,{encoded_image}) no-repeat center center fixed;
            background-size: cover;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.97); 
            padding: 20px;
            margin: 0 auto;
            border-radius: 8px;
            width: 50%; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
