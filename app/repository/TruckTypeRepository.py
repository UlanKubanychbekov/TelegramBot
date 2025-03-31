from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.TruckType import TruckType

class TruckTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(TruckType))
        return result.scalars().all()

    async def get_item(self, truck_type_id: int):
        return await self.db.get(TruckType, truck_type_id)

    async def create(self, truck_type: TruckType):
        self.db.add(truck_type)
        await self.db.commit()
        await self.db.refresh(truck_type)
        return truck_type