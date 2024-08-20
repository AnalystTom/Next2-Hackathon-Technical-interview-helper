from fastapi import FastAPI, HTTPException
from backend.database import init_db, SessionLocal
from backend.models import InterviewQuestion
from backend.interview_questions.question_generator import generate_question
from backend.interview_questions.answer_evaluator import evaluate_answer

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/generate-question/")
def get_question():
    try:
        question = generate_question()
        return {"question": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate-answer/")
def evaluate_user_answer(question_id: int, answer: str):
    try:
        result = evaluate_answer(question_id, answer)
        return {"evaluation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
