import asyncio
from aiogram import Bot

TOKEN = "7805264142:AAH_Mpzda5dAm-bDFuS20eGVRW-GYg7Qo0M"

async def main():
    bot = Bot(token=TOKEN)
    me = await bot.get_me()
    print("Бот найден:")
    print(f"Имя: {me.first_name}")
    print(f"Юзернейм: @{me.username}")
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())


