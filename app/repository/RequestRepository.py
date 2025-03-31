from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Request import Request
from typing import Optional

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

    async def get_by(self, origin: Optional[str] = None, destination: Optional[str] = None, truck_type_id: Optional[int] = None):
        query = select(Request)

        if origin:
            query = query.where(Request.origin == origin)
        if destination:
            query = query.where(Request.destination == destination)
        if truck_type_id:
            query = query.where(Request.truck_type_id == truck_type_id)

        result = await self.db.execute(query)
        return result.scalars().all()
