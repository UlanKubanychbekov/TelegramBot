from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.SpeedTypeService import SpeedTypeService
from app.schemas import SpeedTypeCreate, SpeedType
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/speed_types/", response_model=List[SpeedType], summary="Get all speed types", description="Retrieve a list of all available speed types.")
async def get_speed_types(db: AsyncSession = Depends(get_db)):
    speed_type_service = SpeedTypeService(db)
    speed_types = await speed_type_service.get_list()
    return speed_types

@router.get("/speed_types/{speed_type_id}", response_model=SpeedType, summary="Get speed type by ID", description="Fetch a specific speed type by its unique ID.")
async def get_speed_type(speed_type_id: int, db: AsyncSession = Depends(get_db)):
    speed_type_service = SpeedTypeService(db)
    speed_type = await speed_type_service.get_item(speed_type_id)
    if not speed_type:
        raise HTTPException(status_code=404, detail="Speed type not found")
    return speed_type

@router.post("/speed_types/", response_model=SpeedType, summary="Create a new speed type", description="Create a new speed type and store it in the database.")
async def create_speed_type(speed_type: SpeedTypeCreate, db: AsyncSession = Depends(get_db)):
    speed_type_service = SpeedTypeService(db)
    new_speed_type = await speed_type_service.create(speed_type)
    return new_speed_type
