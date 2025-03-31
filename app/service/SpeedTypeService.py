import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import SpeedTypeCreate
from app.models.SpeedType import SpeedType
from app.repository.SpeedTypeRepository import SpeedTypeRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SpeedTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = SpeedTypeRepository(db)

    async def get_list(self):
        try:
            return await self.repository.get_list()
        except Exception as e:
            logger.error(f"Error fetching speed type list: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_item(self, speed_type_id: int):
        try:
            speed_type = await self.repository.get_item(speed_type_id)
            if not speed_type:
                raise HTTPException(status_code=404, detail="Speed type not found")
            return speed_type
        except Exception as e:
            logger.error(f"Error fetching speed type with ID {speed_type_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create(self, speed_type_create: SpeedTypeCreate):
        try:
            speed_type = SpeedType(
                type_name=speed_type_create.type_name,
                active=speed_type_create.active
            )
            return await self.repository.create(speed_type)
        except Exception as e:
            logger.error(f"Error creating speed type: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")