from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.Employee import Employee
from models.Supplier import Supplier
from models.TruckType import TruckType
from models.SpeedType import SpeedType
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/requests_db")

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронную сессию
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Асинхронная инициализация базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)