import streamlit as st
import requests

st.title("Technical Interview Preparation")

st.header("Generate a New Interview Question")
if st.button("Generate Question"):
    response = requests.post("http://localhost:8000/generate-question/")
    question = response.json().get("question")
    st.write(question)

    st.header("Your Answer")
    user_answer = st.text_area("Type your answer here:")

    if st.button("Submit Answer"):
        question_id = question["id"]
        eval_response = requests.post(
            "http://localhost:8000/evaluate-answer/",
            json={"question_id": question_id, "answer": user_answer}
        )
        evaluation = eval_response.json().get("evaluation")
        st.write(f"Your answer is: {evaluation}")
