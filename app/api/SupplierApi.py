from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.Supplier import Supplier
from schemas import SupplierCreate
from database import get_db

router = APIRouter()

@router.post("/suppliers/")
async def create_supplier(supplier: SupplierCreate, db: AsyncSession = Depends(get_db)):
    new_supplier = Supplier(
        legal_name=supplier.legal_name,
        phone_number=supplier.phone_number,
        telegram_id=supplier.telegram_id
    )
    db.add(new_supplier)
    await db.commit()
    return {"message": "Supplier created successfully!"}

@router.get("/suppliers/")
async def get_suppliers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Supplier))
    suppliers = result.scalars().all()
    return suppliers