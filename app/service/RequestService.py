import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import RequestCreate
from app.models.Request import Request
from app.repository.RequestRepository import RequestRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RequestService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = RequestRepository(db)

    async def get_list(self):
        try:
            return await self.repository.get_list()
        except Exception as e:
            logger.error(f"Error fetching request list: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_item(self, request_id: int):
        try:
            request = await self.repository.get_item(request_id)
            if not request:
                raise HTTPException(status_code=404, detail="Request not found")
            return request
        except Exception as e:
            logger.error(f"Error fetching request with ID {request_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create(self, request_create: RequestCreate):
        try:
            request = Request(
                origin=request_create.origin,
                destination=request_create.destination,
                truck_type_id=request_create.truck_type_id,
                speed_type_id=request_create.speed_type_id,
                created_at=request_create.created_at,
                start_date=request_create.start_date,
                employee_id=request_create.employee_id,
                telegram_message_link=request_create.telegram_message_link
            )
            return await self.repository.create(request)
        except Exception as e:
            logger.error(f"Error creating request: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_by(self, **kwargs):
        try:
            return await self.repository.get_by(**kwargs)
        except Exception as e:
            logger.error(f"Error fetching requests by {kwargs}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")