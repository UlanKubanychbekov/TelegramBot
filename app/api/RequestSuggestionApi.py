from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.RequestSuggestionService import RequestSuggestionService
from app.schemas import RequestSuggestionCreate, RequestSuggestion
from app.database import get_db
from typing import List
router = APIRouter()

@router.get("/suggestions/", response_model=List[RequestSuggestion])
async def get_suggestions(db: AsyncSession = Depends(get_db)):
    suggestion_service = RequestSuggestionService(db)
    return await suggestion_service.get_list()

@router.get("/suggestions/{suggestion_id}", response_model=RequestSuggestion)
async def get_suggestion(suggestion_id: int, db: AsyncSession = Depends(get_db)):
    suggestion_service = RequestSuggestionService(db)
    return await suggestion_service.get_item(suggestion_id)

@router.post("/suggestions/", response_model=RequestSuggestion)
async def create_suggestion(suggestion: RequestSuggestionCreate, db: AsyncSession = Depends(get_db)):
    suggestion_service = RequestSuggestionService(db)
    return await suggestion_service.create(suggestion)