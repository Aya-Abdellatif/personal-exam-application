import streamlit as st

from data_manager import DataManager
from exam_ui import add_background_image, check_answer, get_exams
from session import Session

st.image("img/logo.png", width=200)

st.session_state.session = Session()


def main_page():
    st.title("Student Average Score")

    # Progress Bar and Score Display
    avg_score = DataManager.get_average_score()
    if avg_score is not None:
        progress_bar_value = avg_score / 20
        st.metric(label="Average Score", value=f"{avg_score}/20")
        st.progress(progress_bar_value)

    exam_images = {
        "Exam 1": "img/1.jpeg",  # Replace with actual image paths
        "Exam 2": "img/2.jpeg",  # Replace with actual image paths
        "Exam 3": "img/3.jpeg",  # Replace with actual image paths
    }

    # Create three columns for the images to appear side by side
    col1, col2, col3 = st.columns(3)

    # Action when an image is clicked (as a button)
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


def exam_page(exam_index: int):
    exam = Session.exam
    st.title(f"Welcome to Exam {exam_index + 1}")
    st.write("Welcome to Page 1!")
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
            index=(
                options.index(Session.exam_answers[index])
                if Session.exam_answers[index]
                else None
            ),
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
        for index, question in enumerate(exam):
            correct_answer_char = question.answer
            user_answer = Session.exam_answers[index]
            answer_topics.append(question.topic)

            if check_answer(user_answer, correct_answer_char, question):
                st.success(
                    f"✅ Q{index + 1}: Correct! The answer is **{correct_answer_char}**."
                )
                correct_count += 1
            else:
                st.error(
                    f"❌ Q{index + 1}: Wrong. You chose **{user_answer}**, but the correct answer is **{correct_answer_char}**."
                )
                wrong_topics.append(question.topic)

        st.write(f"### Your Score: {correct_count}/20")

        DataManager.append_transaction(wrong_topics)


if st.session_state.session.exam_index is not None:
    if not Session.exam:
        Session.exam = get_exams()[st.session_state.session.exam_index]
    exam_page(st.session_state.session.exam_index)
else:
    main_page()
