from fastapi import APIRouter, HTTPException
from api.models.schemas import QueryRequest, QueryResponse, ManualInputRequest
from src.generation.answer_generator import ask
from src.user_data.manual_input import build_profile_from_manual_input

router = APIRouter()


@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Ask FitRAG a fitness recovery question.
    Optionally pass a user profile for personalized answers.
    """
    try:
        result = ask(
            question=request.question,
            user_profile=request.user_profile
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask/manual")
async def ask_with_manual_input(
    answers: ManualInputRequest,
    question: str
):
    """
    Ask a question with manual form input.
    Builds user profile from form answers then queries RAG.
    """
    try:
        profile = build_profile_from_manual_input(answers.dict())
        result = ask(
            question=question,
            user_profile=profile
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))