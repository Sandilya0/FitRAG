from pydantic import BaseModel
from typing import Optional


class ManualInputRequest(BaseModel):
    sleep_duration: str
    sleep_quality: str
    alcohol: str
    stress: str
    exercise: str
    exercise_intensity: Optional[str] = "none"
    feeling: str
    additional_factors: Optional[list[str]] = []


class QueryRequest(BaseModel):
    question: str
    user_profile: Optional[dict] = {}


class SourceChunk(BaseModel):
    text: str
    source: str
    page_num: int
    relevance_score: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]
    context_chunks: list[dict]


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str