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

# Создание Router для обработки команд
router = Router()

# Функция для перезапуска бота
async def restart_bot():
    """
    Перезапускает бота.
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Команда /help
@router.message(Command("help"))  # Используем фильтр команд
async def send_help(message: types.Message):
    """
    Обработчик команды /help.
    Отправляет пользователю список доступных команд и их описание.
    """
    help_text = """
    Доступные команды:

    /start - Приветственное сообщение и описание функционала бота.
    /help - Показать список команд и их описание.
    /register_employee - Зарегистрировать сотрудника. Введите ФИО и ID сотрудника через запятую.
    /register_supplier - Зарегистрировать поставщика. Введите наименование юр. лица, телефон и ID через запятую.
    /create_request - Создать заявку на перевозку. Введите данные заявки через запятую: 
                      место отправления, место назначения, ID типа машины, ID типа скорости, дата и время начала, ID сотрудника.
    """
    await message.answer(help_text)


import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
import sys
import os

API_TOKEN = 'your_api_token'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет!!! Я бот для регистрации сотрудников и поставщиков и создания заявок на перевозку.")

@router.message(Command("help"))
async def send_help(message: types.Message):
    help_text = """
    Доступные команды:
    /start - Приветственное сообщение
    /help - Показать список команд
    /register_employee - Зарегистрировать сотрудника
    /register_supplier - Зарегистрировать поставщика
    /create_request - Создать заявку на перевозку
    """
    await message.answer(help_text)

@router.message(Command("register_employee"))
async def register_employee(message: types.Message):
    await message.answer("Пожалуйста, введите ваше полное ФИО и ID через запятую (например, Иванов Иван Иванович, 123456789).")


# Команда /register_supplier
@router.message(Command("register_supplier"))  # Используем фильтр команд
async def register_supplier(message: types.Message):
    """
    Обработчик команды /register_supplier.
    Запрашивает у пользователя наименование юр. лица, телефон и ID поставщика для регистрации.
    """
    await message.answer(
        "Пожалуйста, введите наименование Юр. Лица, номер телефона и ваш ID через запятую (например, ООО Ромашка, 89001234567, 123456789).")


# Обработка сообщения с регистрационными данными (сотрудника или поставщика)
@router.message(lambda message: ',' in message.text)
async def process_registration(message: types.Message):
    """
    Обрабатывает данные, которые пользователь вводит для регистрации сотрудника или поставщика.
    Регистрация сотрудника (2 поля) или поставщика (3 поля).
    """
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


# Команда /create_request
@router.message(Command("create_request"))  # Используем фильтр команд
async def create_request(message: types.Message):
    """
    Обработчик команды /create_request.
    Запрашивает у пользователя данные для создания заявки на перевозку.
    """
    await message.answer(
        "Пожалуйста, введите данные заявки через запятую (например, Москва, Санкт-Петербург, 1, 1, 2025-04-01 12:00:00, 123456789).")


# Обработка сообщения с данными заявки
@router.message(lambda message: ',' in message.text)
async def process_request(message: types.Message):
    """
    Обрабатывает данные заявки, полученные от пользователя.
    Проверяет правильность введенных данных и создает заявку в базе.
    """
    data = message.text.split(',')
    logging.info(f"Данные, полученные от пользователя: {data}")

    if len(data) != 6:
        # Проверка на правильность формата данных (6 полей)
        await message.answer(
            "Ошибка: неверный формат данных. Пожалуйста, убедитесь, что данные разделены запятой и в правильном количестве.")
        return

    try:
        # Извлечение и преобразование данных
        departure, destination, truck_type_id, speed_type_id, start_shipping_date, employee_id = data[0].strip(), data[
            1].strip(), int(data[2].strip()), int(data[3].strip()), data[4].strip(), int(data[5].strip())

        # Преобразуем start_shipping_date в datetime
        start_shipping_date = datetime.datetime.strptime(start_shipping_date, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        logging.error(f"Ошибка при обработке данных: {e}")
        await message.answer("Ошибка: неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD HH:MM:SS.")
        return

    # Создаем новый запрос на перевозку
    try:
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
    except Exception as e:
        logging.error(f"Ошибка при создании заявки: {e}")
        await message.answer(f"Ошибка при создании заявки: {str(e)}")


# Команда для перезапуска бота
@router.message(Command("restart"))  # Используем фильтр команд
async def restart(message: types.Message):
    """
    Обработчик команды /restart для перезапуска бота.
    """
    await message.answer("Перезапускаю бота...")
    await restart_bot()  # Перезапуск бота


# Основная функция
async def main():
    dp.include_router(router)  # Подключаем router к dispatcher
    await dp.start_polling(bot)  # Передаем экземпляр бота в start_polling


if __name__ == "__main__":
    asyncio.run(main())
