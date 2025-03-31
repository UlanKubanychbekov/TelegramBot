from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.SpeedTypeService import SpeedTypeService
from app.schemas import SpeedTypeCreate, SpeedType
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/speed_types/", response_model=List[SpeedType])
async def get_speed_types(db: AsyncSession = Depends(get_db)):
    speed_type_service = SpeedTypeService(db)
    return await speed_type_service.get_list()

@router.get("/speed_types/{speed_type_id}", response_model=SpeedType)
async def get_speed_type(speed_type_id: int, db: AsyncSession = Depends(get_db)):
    speed_type_service = SpeedTypeService(db)
    return await speed_type_service.get_item(speed_type_id)

@router.post("/speed_types/", response_model=SpeedType)
async def create_speed_type(speed_type: SpeedTypeCreate, db: AsyncSession = Depends(get_db)):
    speed_type_service = SpeedTypeService(db)
    return await speed_type_service.create(speed_type)