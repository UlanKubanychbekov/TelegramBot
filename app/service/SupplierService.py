import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import SupplierCreate
from app.models.Supplier import Supplier
from app.repository.SupplierRepository import SupplierRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SupplierService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = SupplierRepository(db)

    async def get_list(self):
        try:
            return await self.repository.get_list()
        except Exception as e:
            logger.error(f"Error fetching supplier list: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_item(self, supplier_id: int):
        try:
            supplier = await self.repository.get_item(supplier_id)
            if not supplier:
                raise HTTPException(status_code=404, detail="Supplier not found")
            return supplier
        except Exception as e:
            logger.error(f"Error fetching supplier with ID {supplier_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create(self, supplier_create: SupplierCreate):
        try:
            supplier = Supplier(
                legal_name=supplier_create.legal_name,
                phone_number=supplier_create.phone_number,
                telegram_id=supplier_create.telegram_id
            )
            return await self.repository.create(supplier)
        except Exception as e:
            logger.error(f"Error creating supplier: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")