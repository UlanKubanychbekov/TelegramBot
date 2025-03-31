from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    truck_type_id = Column(Integer, ForeignKey('truck_types.id'), nullable=False)
    speed_type_id = Column(Integer, ForeignKey('speed_types.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    start_date = Column(DateTime, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    telegram_message_link = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="requests")
    truck_type = relationship("TruckType")
    speed_type = relationship("SpeedType")
    suggestions = relationship("RequestSuggestion", back_populates="request")