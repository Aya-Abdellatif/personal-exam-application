import streamlit as st
import pandas as pd
import base64

from data_manager import DataManager


def check_answer(user_answer: str, correct_answer_char: str, row):
    return user_answer == row[f"choice{correct_answer_char.upper()}"]


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


add_background_image("background.jpg")

data = pd.read_csv("all_data.csv")
answer_topics = []

if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = pd.DataFrame()
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}

if st.session_state.selected_questions.empty:
    st.session_state.selected_questions = data.sample(n=10).reset_index(drop=True)

st.title("📝 Exam Page")
st.markdown("Answer the following questions:")

for index, row in st.session_state.selected_questions.iterrows():
    st.markdown(f"### Q{index + 1}: {row['questionText']}")

    options = [row["choiceA"], row["choiceB"], row["choiceC"], row["choiceD"]]
    if index not in st.session_state.answers:
        st.session_state.answers[index] = None

    st.session_state.answers[index] = st.radio(
        f"Your Answer for Q{index + 1}:",
        options,
        index=(
            options.index(st.session_state.answers[index])
            if st.session_state.answers[index]
            else None
        ),
        key=f"q{index}",
        disabled=st.session_state.submitted,
    )


if st.button("Submit") and not st.session_state.submitted:
    st.session_state.submitted = True
    st.experimental_rerun()

if st.session_state.submitted:
    st.markdown("## Results:")
    correct_count = 0
    wrong_topics = []
    for index, row in st.session_state.selected_questions.iterrows():
        correct_answer_char = row["answer"]
        user_answer = st.session_state.answers[index]
        answer_topics.append(row["subTopic"])

        if check_answer(user_answer, correct_answer_char, row):
            st.success(
                f"✅ Q{index + 1}: Correct! The answer is **{correct_answer_char}**."
            )
            correct_count += 1
        else:
            st.error(
                f"❌ Q{index + 1}: Wrong. You chose **{user_answer}**, but the correct answer is **{correct_answer_char}**."
            )
            wrong_topics.append(row["topic"])

    st.write(
        f"### Your Score: {correct_count}/{len(st.session_state.selected_questions)}"
    )

    DataManager.append_transaction(wrong_topics)
