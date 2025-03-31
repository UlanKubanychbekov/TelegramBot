from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.TruckTypeService import TruckTypeService
from app.schemas import TruckTypeCreate, TruckType
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/truck_types/", response_model=List[TruckType], summary="Get all truck types", description="Retrieve a list of all available truck types.")
async def get_truck_types(db: AsyncSession = Depends(get_db)):
    truck_type_service = TruckTypeService(db)
    truck_types = await truck_type_service.get_list()
    return truck_types

@router.get("/truck_types/{truck_type_id}", response_model=TruckType, summary="Get truck type by ID", description="Fetch a specific truck type by its unique ID.")
async def get_truck_type(truck_type_id: int, db: AsyncSession = Depends(get_db)):
    truck_type_service = TruckTypeService(db)
    truck_type = await truck_type_service.get_item(truck_type_id)
    if not truck_type:
        raise HTTPException(status_code=404, detail="Truck type not found")
    return truck_type

@router.post("/truck_types/", response_model=TruckType, summary="Create a new truck type", description="Create a new truck type and store it in the database.")
async def create_truck_type(truck_type: TruckTypeCreate, db: AsyncSession = Depends(get_db)):
    truck_type_service = TruckTypeService(db)
    new_truck_type = await truck_type_service.create(truck_type)
    return new_truck_type
