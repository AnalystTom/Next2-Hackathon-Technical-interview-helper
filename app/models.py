from pydantic import BaseModel
from typing import List, Optional

class TeamMember(BaseModel):
    name: str
    skills: List[str]

class HackathonInput(BaseModel):
    objective: str
    technologies: List[str]
    judging_criteria: List[str]
    teammates: List[TeamMember]

class ConversationState(BaseModel):
    system_content: str
    messages: List[dict]  # List of message objects to maintain conversation history
