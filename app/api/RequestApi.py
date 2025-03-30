from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.request import Request
from schemas import RequestCreate
from database import get_db

router = APIRouter()

@router.post("/requests/")
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    new_request = Request(
        departure=request.departure,
        destination=request.destination,
        truck_type_id=request.truck_type_id,
        speed_type_id=request.speed_type_id,
        start_shipping_date=request.start_shipping_date,
        employee_id=request.employee_id,
        message_link_tg=request.message_link_tg
    )
    db.add(new_request)
    await db.commit()
    return {"message": "Request created successfully!"}

@router.get("/requests/")
async def get_requests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Request))
    requests = result.scalars().all()
    return requests