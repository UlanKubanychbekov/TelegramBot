from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.SupplierService import SupplierService
from app.schemas import SupplierCreate, Supplier
from app.database import get_db
from typing import List
router = APIRouter()

@router.get("/suppliers/", response_model=List[Supplier])
async def get_suppliers(db: AsyncSession = Depends(get_db)):
    supplier_service = SupplierService(db)
    return await supplier_service.get_list()

@router.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    supplier_service = SupplierService(db)
    return await supplier_service.get_item(supplier_id)

@router.post("/suppliers/", response_model=Supplier)
async def create_supplier(supplier: SupplierCreate, db: AsyncSession = Depends(get_db)):
    supplier_service = SupplierService(db)
    return await supplier_service.create(supplier)