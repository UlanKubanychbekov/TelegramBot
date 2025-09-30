# app/bot/handlers.py
from aiogram import Dispatcher, types

def register_handlers(dp: Dispatcher):
    @dp.message()
    async def echo(message: types.Message):
        await message.answer(f"Вы написали: {message.text}")
