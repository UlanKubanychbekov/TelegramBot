# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не задан в .env!")

# Убедимся, что используется asyncpg
if not DATABASE_URL.startswith("postgresql+asyncpg://"):
    raise RuntimeError("DATABASE_URL должен начинаться с 'postgresql+asyncpg://' для async SQLAlchemy")

# --- Async engine ---
engine = create_async_engine(DATABASE_URL, echo=True)

# --- Async сессия ---
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# --- База ---
Base = declarative_base()

# --- Функции ---
async def reset_db():
    """Полная очистка и пересоздание всех таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def init_db():
    """Инициализация базы, создание таблиц"""
    async with engine.begin() as conn:
        try:
            # Импорт моделей здесь, чтобы избежать циклических импортов
            from app.models import Employee, Request, Supplier, RequestSuggestion, TruckType, SpeedType
            await conn.run_sync(Base.metadata.create_all)
        except SQLAlchemyError as e:
            print(f"Ошибка при инициализации базы: {e}")
            raise

async def get_db():
    """Dependency для FastAPI"""
    async with SessionLocal() as session:
        yield session
