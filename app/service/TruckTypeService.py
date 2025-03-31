import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import TruckTypeCreate
from app.models.TruckType import TruckType
from app.repository.TruckTypeRepository import TruckTypeRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TruckTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = TruckTypeRepository(db)

    async def get_list(self):
        try:
            return await self.repository.get_list()
        except Exception as e:
            logger.error(f"Error fetching truck type list: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_item(self, truck_type_id: int):
        try:
            truck_type = await self.repository.get_item(truck_type_id)
            if not truck_type:
                raise HTTPException(status_code=404, detail="Truck type not found")
            return truck_type
        except Exception as e:
            logger.error(f"Error fetching truck type with ID {truck_type_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create(self, truck_type_create: TruckTypeCreate):
        try:
            truck_type = TruckType(
                type_name=truck_type_create.type_name,
                active=truck_type_create.active
            )
            return await self.repository.create(truck_type)
        except Exception as e:
            logger.error(f"Error creating truck type: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")