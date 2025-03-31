from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.SupplierService import SupplierService
from app.schemas import SupplierCreate, Supplier
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/suppliers/", response_model=List[Supplier], summary="Get all suppliers", description="Retrieve a list of all available suppliers.")
async def get_suppliers(db: AsyncSession = Depends(get_db)):
    supplier_service = SupplierService(db)
    suppliers = await supplier_service.get_list()
    return suppliers

@router.get("/suppliers/{supplier_id}", response_model=Supplier, summary="Get supplier by ID", description="Fetch a specific supplier by its unique ID.")
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    supplier_service = SupplierService(db)
    supplier = await supplier_service.get_item(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.post("/suppliers/", response_model=Supplier, summary="Create a new supplier", description="Create a new supplier and store it in the database.")
async def create_supplier(supplier: SupplierCreate, db: AsyncSession = Depends(get_db)):
    supplier_service = SupplierService(db)
    new_supplier = await supplier_service.create(supplier)
    return new_supplier
