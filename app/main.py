from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router  # This should correctly import the 'router' object

app = FastAPI(
    title="Hackathon Helper API",
    description="API for the Hackathon Helper app, providing brainstorming and planning assistance for hackathons.",
    version="1.0.0"
)

origins = [
    "http://localhost:8501",  # Streamlit default localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon Helper API"}
