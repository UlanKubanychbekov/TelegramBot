# from aiogram import types
# from aiogram.dispatcher.filters import CallbackQueryFilter
#
# class CallbackDataFilter(CallbackQueryFilter):
#     def __init__(self, prefix: str):
#         self.prefix = prefix
#
#     async def check(self, query: types.CallbackQuery) -> bool:
#         return query.data.startswith(self.prefix)
#
# async def example_callback_handler(query: types.CallbackQuery):
#     await query.answer("This is an example callback response.")
#     await query.message.edit_text("Callback data handled.")