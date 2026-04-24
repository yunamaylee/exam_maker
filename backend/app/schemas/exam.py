from typing import Optional, List, Any
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
    question_types: List[str] = []


class GenerateExamRequest(BaseModel):
    passages: PassagesRequest
    options: ExamOptions


# 응답 스키마
class AnalyzeExamResponse(BaseModel):
    success: bool
    analysis_id: str
    analysis_result: dict[str, Any]
    message: str


class ExtractPassagesResponse(BaseModel):
    success: bool
    passages: dict[str, Any]


class GenerateExamResponse(BaseModel):
    success: bool
    exam_id: str
    exam: dict[str, Any]


class DownloadExamResponse(BaseModel):
    success: bool
    exam_id: str


class HealthResponse(BaseModel):
    status: str