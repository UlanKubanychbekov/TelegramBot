import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import RequestSuggestionCreate
from app.models.RequestSuggestion import RequestSuggestion
from app.repository.RequestSuggestionRepository import RequestSuggestionRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RequestSuggestionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = RequestSuggestionRepository(db)

    async def get_list(self):
        try:
            return await self.repository.get_list()
        except Exception as e:
            logger.error(f"Error fetching request suggestion list: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_item(self, suggestion_id: int):
        try:
            suggestion = await self.repository.get_item(suggestion_id)
            if not suggestion:
                raise HTTPException(status_code=404, detail="Request suggestion not found")
            return suggestion
        except Exception as e:
            logger.error(f"Error fetching request suggestion with ID {suggestion_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create(self, suggestion_create: RequestSuggestionCreate):
        try:
            suggestion = RequestSuggestion(
                supplier_id=suggestion_create.supplier_id,
                request_id=suggestion_create.request_id,
                amount=suggestion_create.amount,
                comment=suggestion_create.comment,
                approved=suggestion_create.approved
            )
            return await self.repository.create(suggestion)
        except Exception as e:
            logger.error(f"Error creating request suggestion: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")