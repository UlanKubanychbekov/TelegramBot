from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.TruckTypeService import TruckTypeService
from app.schemas import TruckTypeCreate, TruckType
from app.database import get_db
from typing import List
router = APIRouter()

@router.get("/truck_types/", response_model=List[TruckType])
async def get_truck_types(db: AsyncSession = Depends(get_db)):
    truck_type_service = TruckTypeService(db)
    return await truck_type_service.get_list()

@router.get("/truck_types/{truck_type_id}", response_model=TruckType)
async def get_truck_type(truck_type_id: int, db: AsyncSession = Depends(get_db)):
    truck_type_service = TruckTypeService(db)
    return await truck_type_service.get_item(truck_type_id)

@router.post("/truck_types/", response_model=TruckType)
async def create_truck_type(truck_type: TruckTypeCreate, db: AsyncSession = Depends(get_db)):
    truck_type_service = TruckTypeService(db)
    return await truck_type_service.create(truck_type)