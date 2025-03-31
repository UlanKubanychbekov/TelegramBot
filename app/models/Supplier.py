from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=False)
    telegram_id = Column(String, unique=True, nullable=True)

    request_suggestions = relationship("RequestSuggestion", back_populates="supplier")
