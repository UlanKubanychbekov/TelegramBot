from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# URL подключения к базе данных
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/requests_db"

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессия с асинхронным поддержанием сессий
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для определения моделей
Base = declarative_base()

# Функция для сброса базы данных (удаление и пересоздание таблиц)
async def reset_db():
    async with engine.begin() as conn:
        # Удаление всех таблиц
        await conn.run_sync(Base.metadata.drop_all)
        # Создание всех таблиц
        await conn.run_sync(Base.metadata.create_all)

# Функция для получения сессии из базы данных
async def get_db():
    async with SessionLocal() as session:
        yield session

# Функция для инициализации базы данных (создание таблиц)
async def init_db():
    async with engine.begin() as conn:
        # Импортирование всех моделей, чтобы их таблицы были созданы
        from app.models import Employee, Request, Supplier, RequestSuggestion, TruckType, SpeedType
        await conn.run_sync(Base.metadata.create_all)

