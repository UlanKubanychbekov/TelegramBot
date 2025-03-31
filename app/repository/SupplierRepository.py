from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Supplier import Supplier

class SupplierRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(Supplier))
        return result.scalars().all()

    async def get_item(self, supplier_id: int):
        return await self.db.get(Supplier, supplier_id)

    async def create(self, supplier: Supplier):
        self.db.add(supplier)
        await self.db.commit()
        await self.db.refresh(supplier)
        return supplier