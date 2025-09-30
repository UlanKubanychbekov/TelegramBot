from telethon import TelegramClient
import asyncio

API_ID = 28840201          # замени на свой API_ID
API_HASH = '0aa1f286307d456edef46519b2999de8' # замени на свой API_HASH


async def main():
    async with TelegramClient('./new_userbot_session.session', API_ID, API_HASH) as client:
        print("Сессия создана!")
        me = await client.get_me()
        print(f"Signed in as {me.first_name}")

asyncio.run(main())
