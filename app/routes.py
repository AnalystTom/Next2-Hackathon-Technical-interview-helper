from fastapi import APIRouter, HTTPException
from .models import HackathonInput, ConversationState
import openai
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the APIRouter
router = APIRouter()

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key="9283d831a8164c30b2b64c5830007e2f",
    base_url="https://api.aimlapi.com",
)

@router.post("/start_conversation/")
def start_conversation(input_data: HackathonInput):
    try:
        # Sample data for testing
        system_content = "You are a helpful assistant. Be descriptive and helpful."
        user_content = (
            "Let's start brainstorming for a hackathon. The objective is: Create an AI assistant. "
            "The available technologies are: Llama 3, Python, FastAPI. "
            "Judging criteria include: Innovation, Feasibility. "
            "Team members have the following skills: Alice: Python, Bob: Machine Learning."
        )

        chat_completion = client.chat.completions.create(
            model="lama-3-8b-instruct",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            temperature=0.7,
            max_tokens=512,
        )

        initial_response = chat_completion.choices[0].message.content
        conversation_state = ConversationState(
            system_content=system_content,
            messages=[
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": initial_response}
            ]
        )

        return {"response": initial_response, "conversation_state": conversation_state}

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="Error calling Llama 3 API")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
