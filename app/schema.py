# Flashcard and FlashcardResponse Classes for Flashcard App
from pydantic import BaseModel
from typing import List, Optional

class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardResponse(BaseModel):
    topic:str
    cards: List[Flashcard]