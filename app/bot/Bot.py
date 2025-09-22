#!/usr/bin/env python3
import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# --- Настройка окружения ---
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("Не найден API_TOKEN в .env файле!")



logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()  # роутер создаем один раз

# --- Импорты моделей ---
from app.database import SessionLocal
from app.models.Employee import Employee
from app.models.Request import Request
from app.models.Supplier import Supplier

# --- Хэндлеры команд ---
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Здравствуйте! Я бот для обработки заявок на перевозку.\n"
        "Для просмотра доступных команд нажмите /command."
    )

@router.message(Command("command"))
async def send_command(message: types.Message):
    command_text = """
Доступные команды:
/start - Приветственное сообщение
/command - Показать список команд
/register_employee - Зарегистрировать сотрудника
/register_supplier - Зарегистрировать поставщика
/create_request - Создать заявку
/request_suggestion - Получить предложение по заявке
/restart - Перезапустить бота
"""
    await message.answer(command_text)

@router.message(Command("register_employee"))
async def register_employee(message: types.Message):
    await message.answer("Введите ФИО и ID через запятую (например, Иванов Иван Иванович, 123456789)")

@router.message(Command("register_supplier"))
async def register_supplier(message: types.Message):
    await message.answer("Введите наименование Юр. Лица, телефон и ID через запятую (например, ООО Ромашка, 89001234567, 123456789)")

@router.message(Command("request_suggestion"))
async def request_suggestion(message: types.Message):
    async with SessionLocal() as session:
        suggestions = await session.execute("SELECT * FROM request_suggestions")
        suggestions_list = suggestions.fetchall()
        if suggestions_list:
            response_text = "Возможные варианты заявок:\n"
            for s in suggestions_list:
                response_text += f"{s.departure} -> {s.destination}, Тип машины: {s.truck_type_id}, Тип скорости: {s.speed_type_id}, Дата: {s.start_shipping_date}\n"
        else:
            response_text = "Нет доступных предложений."
        await message.answer(response_text)

@router.message(Command("create_request"))
async def create_request(message: types.Message):
    await message.answer("Введите данные заявки через запятую (Москва, Санкт-Петербург, 1, 1, 2025-04-01 12:00:00, 123456789)")

@router.message(Command("restart"))
async def restart(message: types.Message):
    await message.answer("Перезапускаю бота...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

# --- Логирование всех сообщений для отладки ---
@router.message()
async def log_all_messages(message: types.Message):
    print(f"[LOG] Получено сообщение: {message.text}")

# --- Подключаем роутер и запускаем polling ---
dp.include_router(router)

async def main():
    print("Бот запущен, слушаем команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
