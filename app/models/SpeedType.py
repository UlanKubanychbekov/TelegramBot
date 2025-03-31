from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class SpeedType(Base):
    __tablename__ = "speed_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, nullable=False)
    active = Column(Boolean, default=True)