import streamlit as st

st.image("img/logo.png", width=200)

if "page" not in st.session_state:
    st.session_state.page = "main"  # Default page

def main_page():
    st.title("Student Total Score")
    #Progress Bar and Score Display
    progress_bar_value = (10) / 40
    st.metric(label="Total Score", value=f"{10} / {40 * 10}")
    st.progress(progress_bar_value)

    exam_images = {
        "Exam 1": "img/1.jpeg",  # Replace with actual image paths
        "Exam 2": "img/2.jpeg",  # Replace with actual image paths
        "Exam 3": "img/3.jpeg"   # Replace with actual image paths
    }

    # Create three columns for the images to appear side by side
    col1, col2, col3 = st.columns(3)

    # Action when an image is clicked (as a button)
    exam_option = None
    with col1:
        st.image(exam_images["Exam 1"], use_column_width=True, output_format="JPEG")
        if st.button("Start Exam number 1"):
            exam_option = "Exam 1"
            st.session_state.selected_exam = exam_option

    with col2:
        st.image(exam_images["Exam 2"], use_column_width=True, output_format="JPEG")
        if st.button("Start Exam number 2"):
            exam_option = "Exam 2"
            st.session_state.selected_exam = exam_option
    with col3:
        st.image(exam_images["Exam 3"], use_column_width=True, output_format="JPEG")
        if st.button("Start Exam number 3"):
            exam_option = "Exam 3"
            st.session_state.selected_exam = exam_option

    if "selected_exam" in st.session_state:
        selected_exam = st.session_state.selected_exam
        st.write(f"You have selected {selected_exam}. Now proceeding to the exam page...")

        # Redirect to the respective exam page
        if selected_exam == "Exam 1":
            st.session_state.page = "exam"
        elif selected_exam == "Exam 2":
            # Example of Exam 2 page content
            st.write("Welcome to Exam 2!")
            # Add more content or functions related to Exam 2 here.
        elif selected_exam == "Exam 3":
            # Example of Exam 3 page content
            st.write("Welcome to Exam 3!")
            # Add more content or functions related to Exam 3 here.

def exam_page():
    st.title("Exam 1")
    st.write("Welcome to Page 1!")
    if st.button("Back to Dashboard Page"):
        st.session_state.page = "main"

if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "exam":
    exam_page()