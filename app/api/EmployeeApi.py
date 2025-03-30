from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.Employee import Employee
from schemas import EmployeeCreate
from database import get_db

router = APIRouter()

@router.post("/employees/")
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    new_employee = Employee(name=employee.name, telegram_id=employee.telegram_id)
    db.add(new_employee)
    await db.commit()
    return {"message": "Employee created successfully!"}

@router.get("/employees/")
async def get_employees(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee))
    employees = result.scalars().all()
    return employees