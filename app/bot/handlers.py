# app/bot/handlers.py
from aiogram import Router
from aiogram.types import Message

router = Router()

# Правильный хендлер для aiogram 3.x
@router.message()
async def start_command(message: Message):
    if message.text and message.text.lower() == "/start":
        await message.answer(f"Привет, {message.from_user.first_name}! Бот работает.")

# функция для регистрации роутеров в Dispatcher
def register_handlers(dp):
    dp.include_router(router)
