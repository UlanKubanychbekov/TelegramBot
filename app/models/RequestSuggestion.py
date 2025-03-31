from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class RequestSuggestion(Base):
    __tablename__ = "request_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    request_id = Column(Integer, ForeignKey('requests.id'), nullable=False)
    amount = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    approved = Column(Boolean, default=False)

    request = relationship("Request", back_populates="suggestions")
    supplier = relationship("Supplier", back_populates="request_suggestions")
