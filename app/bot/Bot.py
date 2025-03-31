import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from app.database import SessionLocal
from app.models.Employee import Employee
from app.models.Supplier import Supplier
from app.models.Request import Request
import datetime
from aiogram.filters import Command  # Import Command filter
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_TOKEN = '8011092603:AAEK14WPdvhAyW993xgLjIrpB2tjOpjFXTk'

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера с использованием памяти для хранения
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создание Router
router = Router()


# Обработчики команд
@router.message(Command("start"))  # Используем фильтр команд
async def send_welcome(message: types.Message):
    await message.answer("Привет!!! Я бот для регистрации сотрудников и поставщиков и создания заявок на перевозку.")


@router.message(Command("register_employee"))  # Используем фильтр команд
async def register_employee(message: types.Message):
    await message.answer(
        "Пожалуйста, введите ваше полное ФИО и ID через запятую (например, Иванов Иван Иванович, 123456789).")


@router.message(Command("register_supplier"))  # Используем фильтр команд
async def register_supplier(message: types.Message):
    await message.answer(
        "Пожалуйста, введите наименование Юр. Лица, номер телефона и ваш ID через запятую (например, ООО Ромашка, 89001234567, 123456789).")


@router.message(lambda message: ',' in message.text)
async def process_registration(message: types.Message):
    data = message.text.split(',')
    if len(data) == 2:  # Регистрация сотрудника
        name, telegram_id = data[0].strip(), data[1].strip()

        # Сохраняем нового сотрудника в базе данных
        async with SessionLocal() as session:
            new_employee = Employee(name=name, telegram_id=telegram_id)
            session.add(new_employee)
            await session.commit()
            await message.answer(f"Сотрудник {name} успешно зарегистрирован!")

    elif len(data) == 3:  # Регистрация поставщика
        legal_name, phone_number, telegram_id = data[0].strip(), data[1].strip(), data[2].strip()

        # Сохраняем нового поставщика в базе данных
        async with SessionLocal() as session:
            new_supplier = Supplier(legal_name=legal_name, phone_number=phone_number, telegram_id=telegram_id)
            session.add(new_supplier)
            await session.commit()
            await message.answer(f"Поставщик {legal_name} успешно зарегистрирован!")
    else:
        await message.answer("Ошибка: неверный формат данных.")


@router.message(Command("create_request"))  # Используем фильтр команд
async def create_request(message: types.Message):
    await message.answer(
        "Пожалуйста, введите данные заявки через запятую (например, Москва, Санкт-Петербург, 1, 1, 2025-04-01 12:00:00, 123456789).")


@router.message(lambda message: ',' in message.text and len(message.text.split(',')) == 6)
async def process_request(message: types.Message):
    data = message.text.split(',')
    departure, destination, truck_type_id, speed_type_id, start_shipping_date, employee_id = data[0].strip(), data[
        1].strip(), int(data[2].strip()), int(data[3].strip()), data[4].strip(), int(data[5].strip())
    start_shipping_date = datetime.datetime.strptime(start_shipping_date, '%Y-%m-%d %H:%M:%S')

    # Создаем новый запрос на перевозку
    async with SessionLocal() as session:
        new_request = Request(
            departure=departure,
            destination=destination,
            truck_type_id=truck_type_id,
            speed_type_id=speed_type_id,
            start_shipping_date=start_shipping_date,
            employee_id=employee_id
        )
        session.add(new_request)
        await session.commit()
        await message.answer(f"Заявка на перевозку из {departure} в {destination} успешно создана!")


# Основная функция
async def main():
    dp.include_router(router)  # Подключаем router к dispatcher
    await dp.start_polling(bot)  # Передаем экземпляр бота в start_polling


if __name__ == "__main__":
    asyncio.run(main())