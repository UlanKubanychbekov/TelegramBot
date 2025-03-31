import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import EmployeeCreate
from app.models.Employee import Employee
from app.repository import EmployeeRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class EmployeeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = EmployeeRepository(db)

    async def get_list(self):
        try:
            return await self.repository.get_list()
        except Exception as e:
            logger.error(f"Error fetching employee list: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_item(self, employee_id: int):
        try:
            employee = await self.repository.get_item(employee_id)
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            return employee
        except Exception as e:
            logger.error(f"Error fetching employee with ID {employee_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create(self, employee_create: EmployeeCreate):
        try:
            employee = Employee(
                name=employee_create.name,
                active=employee_create.active,
                telegram_id=employee_create.telegram_id
            )
            return await self.repository.create(employee)
        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
