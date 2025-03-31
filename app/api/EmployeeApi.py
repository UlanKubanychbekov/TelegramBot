from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, init_db, engine, Base
from app.schemas import EmployeeCreate, Employee
from app.service.EmployeeService import EmployeeService

router = APIRouter()

@router.get("/employees/", response_model=List[Employee], summary="Get all employees", description="Fetch a list of all employees from the database.")
async def get_employees(db: AsyncSession = Depends(get_db)):
    employee_service = EmployeeService(db)
    employees = await employee_service.get_list()
    return employees

@router.get("/employees/{employee_id}", response_model=Employee, summary="Get employee by ID", description="Fetch a specific employee by their unique ID.")
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_item(employee_id)
    return employee

@router.post("/employees/", response_model=Employee, summary="Create a new employee", description="Create a new employee record in the database.")
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    employee_service = EmployeeService(db)
    new_employee = await employee_service.create(employee)
    return new_employee

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
