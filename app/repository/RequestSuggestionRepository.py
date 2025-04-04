from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.RequestSuggestion import RequestSuggestion

class RequestSuggestionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(RequestSuggestion))
        return result.scalars().all()

    async def get_item(self, suggestion_id: int):
        return await self.db.get(RequestSuggestion, suggestion_id)

    async def create(self, suggestion: RequestSuggestion):
        self.db.add(suggestion)
        await self.db.commit()
        await self.db.refresh(suggestion)
        return suggestion