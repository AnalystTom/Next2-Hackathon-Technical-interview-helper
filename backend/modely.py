from sqlalchemy import Column, Integer, String
from backend.database import Base

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    correct_answer = Column(String)
