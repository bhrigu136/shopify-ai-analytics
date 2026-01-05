from pydantic import BaseModel
from typing import Optional

class AskRequest(BaseModel):
    store_id: str
    question: str

class AskResponse(BaseModel):
    answer: str
    confidence: str  # low|medium|high
    debug: Optional[dict] = None
