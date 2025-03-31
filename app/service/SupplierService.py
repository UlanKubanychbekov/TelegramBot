from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Supplier import Supplier
from sqlalchemy.future import select


class SupplierService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(Supplier))
        return result.scalars().all()

    async def get_item(self, supplier_id: int):
        return await self.db.get(Supplier, supplier_id)