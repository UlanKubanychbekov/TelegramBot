from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Request import Request

class RequestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(Request))
        return result.scalars().all()

    async def get_item(self, request_id: int):
        return await self.db.get(Request, request_id)

    async def get_by(self, **kwargs):
        result = await self.db.execute(select(Request).filter_by(**kwargs))
        return result.scalars().all()