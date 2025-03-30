from pydantic import BaseModel
import datetime

class EmployeeCreate(BaseModel):
    name: str
    telegram_id: str

class SupplierCreate(BaseModel):
    legal_name: str
    phone_number: str
    telegram_id: str

class RequestCreate(BaseModel):
    departure: str
    destination: str
    truck_type_id: int
    speed_type_id: int
    start_shipping_date: datetime.datetime
    employee_id: int
    message_link_tg: str = None

class RequestSuggestionCreate(BaseModel):
    supplier_id: int
    request_id: int
    order_amount: float
    comment: str = None
    approve: bool = False