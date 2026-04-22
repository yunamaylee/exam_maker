from typing import Optional, List
from pydantic import BaseModel


class Passage(BaseModel):
    label: str
    original_type: str
    text: str
    topic: str


class PassagesRequest(BaseModel):
    passages: List[Passage]


class ExamOptions(BaseModel):
    multiple_choice: int
    subjective: int
    difficulty: Optional[str] = None


class GenerateExamRequest(BaseModel):
    passages: PassagesRequest
    options: ExamOptions