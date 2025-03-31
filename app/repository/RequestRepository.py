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

    async def create(self, request: Request):
        self.db.add(request)
        await self.db.commit()
        await self.db.refresh(request)
        return request

    async def get_by(self, **kwargs):
        query = select(Request).filter_by(**kwargs)
        result = await self.db.execute(query)
        return result.scalars().all()