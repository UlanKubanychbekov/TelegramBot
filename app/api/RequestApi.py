from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.RequestService import RequestService
from app.schemas import RequestCreate, Request
from app.database import get_db
from typing import List
router = APIRouter()

@router.get("/requests/", response_model=List[Request])
async def get_requests(db: AsyncSession = Depends(get_db)):
    request_service = RequestService(db)
    return await request_service.get_list()

@router.get("/requests/{request_id}", response_model=Request)
async def get_request(request_id: int, db: AsyncSession = Depends(get_db)):
    request_service = RequestService(db)
    return await request_service.get_item(request_id)

@router.get("/requests/by/", response_model=List[Request])
async def get_requests_by(db: AsyncSession = Depends(get_db), **kwargs):
    request_service = RequestService(db)
    return await request_service.get_by(**kwargs)

@router.post("/requests/", response_model=Request)
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    request_service = RequestService(db)
    return await request_service.create(request)