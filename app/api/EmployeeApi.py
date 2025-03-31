from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.EmployeeService import EmployeeService
from app.schemas import EmployeeCreate, Employee
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/employees/", response_model=List[Employee])
async def get_employees(db: AsyncSession = Depends(get_db)):
    employee_service = EmployeeService(db)
    return await employee_service.get_list()

@router.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee_service = EmployeeService(db)
    return await employee_service.get_item(employee_id)

@router.post("/employees/", response_model=Employee)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    employee_service = EmployeeService(db)
    return await employee_service.create(employee)