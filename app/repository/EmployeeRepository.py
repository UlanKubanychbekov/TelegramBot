from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Employee import Employee

class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self):
        result = await self.db.execute(select(Employee))
        return result.scalars().all()

    async def get_item(self, employee_id: int):
        return await self.db.get(Employee, employee_id)