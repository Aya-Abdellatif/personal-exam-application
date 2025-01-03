import streamlit as st
import pandas as pd
import plotly.express as px

from data_manager import DataManager
from exam_maker import Question, ExamMaker
from frequent_pattern import FrequentPatternManager

import base64
from session import Session

st.image("img/logo.png", width=200)

st.session_state.session = Session()


def get_exams() -> list[list[Question]]:
    transactions = DataManager.load_and_sort_transactions()
    fp_tree = FrequentPatternManager.build_fp_tree(transactions)
    frequent_patterns = FrequentPatternManager.mine_fp_tree(fp_tree.header_table, 2)
    filtered_patterns = FrequentPatternManager.filter_items_with_duplicates(
        frequent_patterns
    )
    return ExamMaker.get_exams(3, filtered_patterns)


def check_answer(user_answer: str, correct_answer_char: str, question: Question) -> bool:
    return user_answer == getattr(question, f"choice_{correct_answer_char}")


def add_background_image(image_file: str) -> None:
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


def main_page():
    st.title("Student Average Score")
    avg_score = DataManager.get_average_score()
    if avg_score is not None:
        progress_bar_value = avg_score / 20
        st.metric(label="Average Score", value=f"{avg_score}/20")
        st.progress(progress_bar_value)

    exam_images = {
        "Exam 1": "img/1.jpeg",
        "Exam 2": "img/2.jpeg",
        "Exam 3": "img/3.jpeg",
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(exam_images["Exam 1"], use_container_width=True, output_format="JPEG")
        if st.button("Start Exam number 1"):
            Session.exam_index = 0
            st.rerun()

    with col2:
        st.image(exam_images["Exam 2"], use_container_width=True, output_format="JPEG")
        if st.button("Start Exam number 2"):
            Session.exam_index = 1
            st.rerun()
    with col3:
        st.image(exam_images["Exam 3"], use_container_width=True, output_format="JPEG")
        if st.button("Start Exam number 3"):
            Session.exam_index = 2
            st.rerun()


def exam_page(exam_index: int) -> None:
    exam = Session.exam
    st.title(f"Welcome to Exam {exam_index + 1}")
    if st.button("Back to Dashboard Page"):
        Session.reset()
        st.rerun()

    add_background_image("img/background2.jpeg")

    answer_topics = []

    st.title("📝 Exam Page")
    st.markdown("Answer the following questions:")

    for index, question in enumerate(exam):
        st.markdown(f"### Q{index + 1}: {question.question_text}")

        options = [
            question.choice_a,
            question.choice_b,
            question.choice_c,
            question.choice_d,
        ]

        Session.exam_answers[index] = st.radio(
            f"Your Answer for Q{index + 1}:",
            options,
            index=(options.index(Session.exam_answers[index]) if Session.exam_answers[index] else None),
            key=f"q{index}",
            disabled=Session.submitted_exam,
        )

    if st.button("Submit") and not Session.submitted_exam:
        Session.submitted_exam = True
        st.rerun()

    if Session.submitted_exam:
        st.markdown("## Results:")
        correct_count = 0
        wrong_topics = []
        correct_topics = {}
        for index, question in enumerate(exam):
            correct_answer_char = question.answer
            user_answer = Session.exam_answers[index]
            answer_topics.append(question.topic)

            if check_answer(user_answer, correct_answer_char, question):
                st.success(
                    f"✅ Q{index + 1}: Correct! The answer is **{correct_answer_char}**."
                )
                correct_count += 1
                correct_topics[question.topic] = correct_topics.get(question.topic, 0) + 1
            else:
                st.error(
                    f"❌ Q{index + 1}: Wrong. You chose **{user_answer}**, but the correct answer is **{correct_answer_char}**."
                )
                wrong_topics.append(question.topic)

        st.write(f"### Your Score: {correct_count}/20")
        DataManager.append_transaction(wrong_topics)

        # Aggregate data for visualization
        wrong_count = pd.Series(wrong_topics).value_counts()
        correct_count = pd.Series(correct_topics).fillna(0)

        df = pd.DataFrame({
            "Topic": wrong_count.index.union(correct_count.index),
            "Correct Answers": correct_count,
            "Wrong Answers": wrong_count,
        }).fillna(0)

        # Visualization
        st.markdown("### Visualization of Your Performance")
        if not df.empty:
            bar_fig = px.bar(
                df,
                x="Topic",
                y=["Correct Answers", "Wrong Answers"],
                barmode="group",
                title="Performance by Topic",
                labels={"value": "Number of Questions", "variable": "Answer Type"},
                text_auto=True,
                color="variable",  # This will automatically color the bars based on the 'variable' column (Correct or Wrong)
                color_discrete_map={
                    "Correct Answers": "green",  # Color for correct answers
                    "Wrong Answers": "red"      # Color for wrong answers
                } 
            )
            st.plotly_chart(bar_fig, use_container_width=True)
        else:
            st.info("No data available for visualization.")


if st.session_state.session.exam_index is not None:
    if not Session.exam:
        Session.exam = get_exams()[st.session_state.session.exam_index]
    exam_page(st.session_state.session.exam_index)
else:
    main_page()