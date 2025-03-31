from sqlalchemy.ext.asyncio import AsyncSession
from app.models.SpeedType import SpeedType
from sqlalchemy.future import select


class SpeedTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(SpeedType))
        return result.scalars().all()

    async def get_item(self, speed_type_id: int):
        return await self.db.get(SpeedType, speed_type_id)