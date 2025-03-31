import asyncio
from datetime import datetime
import logging
import os
import sys

from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from app.database import SessionLocal
from app.models.Employee import Employee
from app.models.Request import Request
from app.models.Supplier import Supplier

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
API_TOKEN = '8011092603:AAGDvX5_WHCu6JuDyIVDOys6JqKfj_OcZRg'

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()


async def restart_bot():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    welcome_text = "Здравствуйте! Я бот для обработки заявок на перевозку.\n" \
                   "Для просмотра доступных команд нажмите /command."
    await message.answer(welcome_text)


@router.message(Command("command"))
async def send_command(message: types.Message):
    command_text = """
    Доступные команды:
    /start - Приветственное сообщение и описание функционала бота.
    /command - Показать список команд и их описание.
    /register_employee - Зарегистрировать сотрудника. Введите ФИО и ID сотрудника через запятую.
    /register_supplier - Зарегистрировать поставщика. Введите наименование юр. лица, телефон и ID через запятую.
    /create_request - Создать заявку на перевозку. Введите данные заявки через запятую: 
            место отправления, место назначения, ID типа машины, ID типа скорости, дата и время начала, ID сотрудника.
    /request_suggestion - Получить предложение по созданию заявки на перевозку.
    """
    await message.answer(command_text)


@router.message(Command("register_employee"))
async def register_employee(message: types.Message):
    await message.answer(
        "Пожалуйста, введите ваше полное ФИО и ID через запятую (например, Иванов Иван Иванович, 123456789).")


@router.message(Command("register_supplier"))
async def register_supplier(message: types.Message):
    await message.answer(
        "Пожалуйста, введите наименование Юр. Лица, номер телефона и ваш ID через запятую (например, ООО Ромашка, 89001234567, 123456789).")


@router.message(Command("request_suggestion"))
async def request_suggestion(message: types.Message):
    async with SessionLocal() as session:
        suggestions = await session.execute("SELECT * FROM request_suggestions")
        suggestions_list = suggestions.fetchall()
        if suggestions_list:
            response_text = "Возможные варианты заявок:\n"
            for suggestion in suggestions_list:
                response_text += f"{suggestion.departure} -> {suggestion.destination}, Тип машины: {suggestion.truck_type_id}, Тип скорости: {suggestion.speed_type_id}, Дата: {suggestion.start_shipping_date}\n"
        else:
            response_text = "Нет доступных предложений."
        await message.answer(response_text)


@router.message(lambda message: message.text.startswith("Регистрация,"))
async def process_registration(message: types.Message):
    data = message.text.split(',')
    if len(data) == 3:
        name, telegram_id = data[0].strip(), data[1].strip()
        async with SessionLocal() as session:
            new_employee = Employee(name=name, telegram_id=telegram_id)
            session.add(new_employee)
            await session.commit()
            await message.answer(f"Сотрудник {name} успешно зарегистрирован!")
    elif len(data) == 4:
        legal_name, phone_number, telegram_id = data[0].strip(), data[1].strip(), data[2].strip()
        async with SessionLocal() as session:
            new_supplier = Supplier(legal_name=legal_name, phone_number=phone_number, telegram_id=telegram_id)
            session.add(new_supplier)
            await session.commit()
            await message.answer(f"Поставщик {legal_name} успешно зарегистрирован!")
    else:
        await message.answer("Ошибка: неверный формат данных. Ожидаются 2 или 3 значения через запятую.")

@router.message(Command("create_request"))
async def create_request(message: types.Message):
    await message.answer(
        "Пожалуйста, введите данные заявки через запятую (например, Москва, Санкт-Петербург, 1, 1, 2025-04-01 12:00:00, 123456789).")

@router.message(lambda message: message.text.startswith("Заявка,"))
async def process_request(message: types.Message):
    data = [part.strip() for part in message.text[7:].split(',')]
    logging.info(f"Данные, полученные от пользователя: {data}")

    if len(data) != 6:
        await message.answer(
            "Ошибка: неверный формат данных. Пожалуйста, убедитесь, что данные разделены запятой и в правильном количестве."
        )
        return

    try:
        origin, destination, truck_type_id, speed_type_id, start_date, employee_id = (
            data[0],
            data[1],
            int(data[2]),
            int(data[3]),
            data[4],
            int(data[5])
        )

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                logging.error(f"Ошибка при обработке даты: неверный формат даты {start_date}")
                await message.answer(
                    "Ошибка: неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD HH:MM:SS или YYYY-MM-DD."
                )
                return

        chat_id = message.chat.id
        message_id = message.message_id

        message_link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{message_id}"

        async with SessionLocal() as session:
            new_request = Request(
                origin=origin,
                destination=destination,
                truck_type_id=truck_type_id,
                speed_type_id=speed_type_id,
                created_at=datetime.utcnow(),
                start_date=start_date,
                employee_id=employee_id,
                telegram_message_link=message_link
            )
            session.add(new_request)
            await session.commit()

            await message.answer(f"✅ Заявка на перевозку из {origin} в {destination} успешно создана!\n📌 [Ссылка на сообщение]({message_link})", parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Ошибка при создании заявки: {e}")
        await message.answer(f"Ошибка при создании заявки: {str(e)}")


@router.message(Command("restart"))
async def restart(message: types.Message):
    await message.answer("Перезапускаю бота...")
    await restart_bot()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
