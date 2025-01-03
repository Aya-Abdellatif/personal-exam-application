# OWLs - Personal Exam Application  

OWLs is a **Personalized Exam Application** designed to provide students with tailored exams and detailed performance feedback. By combining frequent pattern mining and intelligent exam generation, OWLs makes the study process engaging and efficient. The platform features a user-friendly interface built using **Streamlit**.

---

## Features  

- **Personalized Exam Generation:**  
  Automatically generates three unique exams based on predefined topics using frequent pattern mining. Each exam contains:  
  - 14 questions derived from common topic patterns.  
  - 6 questions randomly selected from all topics.

- **Performance Analytics:**  
  After completing an exam, students receive detailed feedback on their answers, including:  
  - Correct and incorrect answers.  
  - Performance visualization by topic.  

- **Frequent Pattern Mining:**  
  OWLs utilizes the FP-tree algorithm to analyze student mistakes and generate frequent topic patterns, ensuring exams are personalized and effective.

- **Interactive UI:**  
  Built using [Streamlit](https://streamlit.io/), OWLs offers an engaging interface for students to:  
  - Select and start exams.  
  - Answer questions with real-time feedback.  
  - View performance metrics and visualizations.

---

## How It Works  

1. **Data Preparation:**  
   - OWLs uses a transaction-based dataset that tracks students' incorrect answers by topic.  
   - Frequent patterns of incorrect answers are mined to identify key topics for exam generation.

2. **Exam Generation:**  
   - Based on frequent patterns and predefined topics, OWLs creates three 20-question exams:
     - 14 questions from common patterns.  
     - 6 randomly selected questions.

3. **Student Interaction:**  
   - Students select an exam from the UI and answer questions.  
   - After submission, the system provides a detailed performance breakdown and visualization.

4. **Feedback Loop:**  
   - Incorrect answers are appended to the transaction database, refining future exam patterns.

---

## Project Structure

```
personal-exam-application/
├── .idea/ 
├── Data Mining Project/          # Main project folder containing all code files
|   ├── data_manager.py           # Manages questions and topics.
|   ├── question.py               # Defines the Question class.
|   ├── frequent_pattern.py       # Implements FP-tree and pattern mining.
|   ├── exam_maker.py             # Handles exam creation logic.
│   ├── session.py                # Session management for UI
|   ├── student_dashboard.py      # Streamlit-based UI.
│   ├── img/                      # Images for UI
|   ├── test_data_manager.py      # Unit tests.
│   ├── test_exam_maker.py        # Unit tests.
│   ├── test_frequent_pattern.py  # Unit tests.
|   ├── requirements.txt          # Requirements file.
├── README.md                     # Documentation.
```

-----

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Aya-Abdellatif/personal-exam-application.git
   cd personal-exam-application
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run student_dashboard.py
   ```

---

## Contribution

We welcome contributions! If you have ideas or find bugs, feel free to open an issue or submit a pull request.

---

## Acknowledgments

Special thanks to the team for their hard work and dedication to making OWLs a reality. 🚀


