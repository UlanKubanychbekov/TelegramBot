# from aiogram import Dispatcher, types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Command
# from aiogram.types import ParseMode
# from aiogram.types import CallbackQuery
# from callbacks import callback_handler
#
# async def start_command(message: types.Message):
#     await message.answer("Welcome! Use /help to get the list of available commands.")
#
# async def help_command(message: types.Message):
#     await message.answer("Available commands:\n/start - Start the bot\n/help - Get help")
#
# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(start_command, Command("start"))
#     dp.register_message_handler(help_command, Command("help"))
#     dp.register_callback_query_handler(callback_handler)