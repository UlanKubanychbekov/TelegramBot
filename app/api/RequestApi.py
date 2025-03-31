from typing import List
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import RequestCreate, Request
from app.service.RequestService import RequestService

router = APIRouter()


@router.get("/requests/", response_model=List[Request], summary="Get all requests",
            description="Retrieve a list of all requests from the database.")
async def get_requests(db: AsyncSession = Depends(get_db)):
    request_service = RequestService(db)
    requests = await request_service.get_list()
    return requests


@router.get("/requests/{request_id}", response_model=Request, summary="Get request by ID",
            description="Fetch a specific request by its unique ID.")
async def get_request(request_id: int, db: AsyncSession = Depends(get_db)):
    request_service = RequestService(db)
    request = await request_service.get_item(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.get("/requests/by/", response_model=List[Request], summary="Get requests by filters", description="Retrieve requests based on the provided filters.")
async def get_requests_by(
    db: AsyncSession = Depends(get_db),
    field1: Optional[str] = Query(None, description="Origin location to filter requests"),
    field2: Optional[int] = Query(None, description="Truck type ID to filter requests"),
    field3: Optional[str] = Query(None, description="Destination location to filter requests'"),
):
    request_service = RequestService(db)
    filters = {
        "origin": field1,
        "truck_type_id": field2,
        "destination": field3,
    }
    requests = await request_service.get_by(**filters)
    return requests



@router.post("/requests/", response_model=Request, summary="Create a new request",
             description="Create a new request in the database.")
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    request_service = RequestService(db)
    new_request = await request_service.create(request)
    return new_request
