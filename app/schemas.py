from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EmployeeBase(BaseModel):
    name: str
    active: Optional[bool] = True
    telegram_id: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode= True

class SupplierBase(BaseModel):
    legal_name: str
    active: Optional[bool] = True
    phone_number: str
    telegram_id: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        orm_mode: True

class RequestBase(BaseModel):
    origin: str
    destination: str
    truck_type_id: int
    speed_type_id: int
    created_at: datetime
    start_date: datetime
    employee_id: int
    telegram_message_link: Optional[str] = None

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int

    class Config:
        orm_mode: True

class RequestSuggestionBase(BaseModel):
    supplier_id: int
    request_id: int
    amount: float
    comment: Optional[str] = None
    approved: Optional[bool] = False

class RequestSuggestionCreate(RequestSuggestionBase):
    pass

class RequestSuggestion(RequestSuggestionBase):
    id: int

    class Config:
        orm_mode: True

class TruckTypeBase(BaseModel):
    type_name: str
    active: Optional[bool] = True

class TruckTypeCreate(TruckTypeBase):
    pass

class TruckType(TruckTypeBase):
    id: int

    class Config:
        orm_mode: True

class SpeedTypeBase(BaseModel):
    type_name: str
    active: Optional[bool] = True

class SpeedTypeCreate(SpeedTypeBase):
    pass

class SpeedType(SpeedTypeBase):
    id: int

    class Config:
        orm_mode: True