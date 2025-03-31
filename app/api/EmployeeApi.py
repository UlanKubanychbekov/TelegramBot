from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.EmployeeService import EmployeeService
from app.schemas import EmployeeCreate, Employee
from app.database import get_db, init_db, engine, Base
from typing import List
from contextlib import asynccontextmanager

router = APIRouter()


@router.get("/employees/", response_model=List[Employee])
async def get_employees(db: AsyncSession = Depends(get_db)):
    print("Initializing database...", flush=True)
    employee_service = EmployeeService(db)
    print("EmployeeService created")
    employees = await employee_service.get_list()
    print("Employees fetched:", employees)
    return employees


@router.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    print(f"Executing get_employee for employee_id={employee_id}")
    employee_service = EmployeeService(db)
    print("EmployeeService created")
    employee = await employee_service.get_item(employee_id)
    print(f"Employee fetched: {employee}")
    return employee

@router.post("/employees/", response_model=Employee)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    print("Executing create_employee")
    employee_service = EmployeeService(db)
    print("EmployeeService created")
    new_employee = await employee_service.create(employee)
    print(f"Employee created: {new_employee}")
    return new_employee


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db()
    print("Database initialized")
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(router)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)