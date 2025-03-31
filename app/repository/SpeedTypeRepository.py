from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.SpeedType import SpeedType

class SpeedTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(SpeedType))
        return result.scalars().all()

    async def get_item(self, speed_type_id: int):
        return await self.db.get(SpeedType, speed_type_id)

    async def create(self, speed_type: SpeedType):
        self.db.add(speed_type)
        await self.db.commit()
        await self.db.refresh(speed_type)
        return speed_type