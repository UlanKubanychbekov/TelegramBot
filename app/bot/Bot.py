import os
import datetime
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, types, functions
from telethon.tl.types import InputMessagesFilterEmpty, InputPeerEmpty
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USERBOT_SESSION = "userbot_session"

userbot = TelegramClient("userbot_session_old", API_ID, API_HASH)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Bishkek"))

DAILY_LIMIT_GROUPS = 30
state = {
    "sent_count": 0,
    "sent_groups": set(),
    "last_reset": datetime.date.today(),
    "last_text": None,
    "mode": None,
    "search_results": [],
}

def reset_if_new_day():
    today = datetime.date.today()
    if today != state["last_reset"]:
        state["sent_count"] = 0
        state["sent_groups"] = set()
        state["last_reset"] = today

async def send_with_limit(entity, text):
    reset_if_new_day()
    group_id = getattr(entity, "id", None)
    if group_id in state["sent_groups"]:
        return False, f"⏩ Уже отправляли сегодня в: {getattr(entity,'title',entity.id)}"
    if state["sent_count"] >= DAILY_LIMIT_GROUPS:
        return False, "❌ Лимит сообщений на сегодня исчерпан"
    try:
        await userbot.send_message(entity, text)
        state["sent_groups"].add(group_id)
        state["sent_count"] += 1
        return True, f"✅ Отправлено в {getattr(entity,'title',entity.id)}"
    except Exception as e:
        return False, f"❌ Ошибка в {getattr(entity,'title',entity.id)}: {e}"

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отправка во все группы", callback_data="send_all")],
            [
                InlineKeyboardButton(text="Поиск групп", callback_data="search"),
                InlineKeyboardButton(text="Поиск объявлений", callback_data="search_msgs"),
            ],
            [
                InlineKeyboardButton(text="Отправка по названию", callback_data="send_by_name"),
                InlineKeyboardButton(text="Лимит", callback_data="limit")
            ],
            [InlineKeyboardButton(text="Глобальный поиск групп", callback_data="global_search")]
        ]
    )

async def global_search_all(userbot, query):
    now = datetime.datetime.utcnow()
    one_day_ago = now - datetime.timedelta(days=1)
    matches = []

    try:
        found = await userbot(functions.contacts.SearchRequest(q=query, limit=10))
        for chat in found.chats:
            title = getattr(chat, "title", "❌ Без названия")
            link = f"https://t.me/{chat.username}" if getattr(chat, "username", None) else "❌ Без ссылки"
            matches.append((f"🌐 Канал/группа: {title}", "", link))
    except Exception as e:
        matches.append((f"❌ Ошибка поиска чатов: {e}", "", None))

    try:
        result = await userbot(functions.messages.SearchGlobalRequest(
            q=query,
            filter=InputMessagesFilterEmpty(),
            min_date=one_day_ago,
            max_date=now,
            offset_rate=0,
            offset_peer=InputPeerEmpty(),
            offset_id=0,
            limit=50
        ))

        for msg in result.messages:
            try:
                peer = await userbot.get_entity(msg.peer_id)
                chat_title = getattr(peer, "title", getattr(peer, "first_name", str(peer.id)))
                snippet = msg.message[:150] if msg.message else ""
                if getattr(peer, "username", None):
                    link = f"https://t.me/{peer.username}/{msg.id}"
                elif getattr(peer, "id", None):
                    link = f"https://t.me/c/{abs(peer.id)}/{msg.id}"
                else:
                    link = None
                matches.append((f"💬 {chat_title}", snippet, link))
            except Exception:
                continue
    except Exception as e:
        matches.append((f"❌ Ошибка поиска сообщений: {e}", "", None))

    return matches

@dp.message(F.text == "/start")
async def start_bot(message: Message):
    await message.answer("🚛 Привет! Выберите действие:", reply_markup=main_menu())

@dp.callback_query()
async def process_callback(callback: CallbackQuery):
    action = callback.data
    if action == "send_all":
        await callback.message.answer("✏️ Напишите текст для массовой рассылки:")
        state["mode"] = "send_all"
    elif action == "send_by_name":
        await callback.message.answer("🔍 Введите ключевое слово для поиска групп или каналов:")
        state["mode"] = "send_by_name"
    elif action == "search":
        await callback.message.answer("🔍 Введите ключевое слово для поиска групп (только среди доступных вам чатов):")
        state["mode"] = "search_mode"
    elif action == "search_msgs":
        await callback.message.answer("🔍 Введите слово для поиска объявлений (за 3 дня, минимум 5 символов):")
        state["mode"] = "search_msgs"
    elif action == "global_search":
        await callback.message.answer("🔍 Введите текст для глобального поиска групп (не менее 6 символов):")
        state["mode"] = "global_search"
    elif action == "limit":
        reset_if_new_day()
        left = DAILY_LIMIT_GROUPS - state["sent_count"]
        await callback.message.answer(f"Сегодня отправлено: {state['sent_count']}\nОстаток лимита: {left}")

@dp.message()
async def handle_text(message: Message):
    text = message.text.strip()
    reset_if_new_day()
    mode = state.get("mode")

    if mode in ["search_msgs", "global_search"] and len(text) < 6:
        await message.answer("❌ Слишком короткий текст для поиска. Минимум 6 символов.")
        return

    dialogs = await userbot.get_dialogs()
    chats = [d.entity for d in dialogs
             if isinstance(d.entity, (types.Chat, types.Channel)) and 
             (not isinstance(d.entity, types.Channel) or d.entity.megagroup or d.entity.broadcast)]

    if mode == "send_all":
        state["last_text"] = text
        results = [await send_with_limit(g, text) for g in chats]
        await message.answer("\n".join([msg for success, msg in results][:20]))
        state["mode"] = None

    elif mode == "send_by_name":
        matched = [g for g in chats if text.lower() in g.title.lower()]
        if not matched:
            await message.answer("❌ Группы или каналы не найдены")
        else:
            state["search_results"] = matched
            state["mode"] = "send_by_name_text"
            await message.answer(
                f"Найдено {len(matched)}:\n" +
                "\n".join([f"📌 {g.title}" for g in matched[:20]]) +
                "\n\n✏️ Введите текст для отправки во все эти чаты:"
            )
    elif mode == "send_by_name_text":
        results = [await send_with_limit(g, text) for g in state["search_results"]]
        await message.answer("\n".join([msg for success, msg in results][:20]))
        state["mode"] = None
        state["search_results"] = []

    elif mode == "search_mode":
        matched = [g for g in chats if text.lower() in g.title.lower()]
        if not matched:
            await message.answer("❌ Группы не найдены")
        else:
            await message.answer(f"Найдено {len(matched)}:\n" + "\n".join([f"📌 {g.title}" for g in matched[:20]]))
        state["mode"] = None

    elif mode == "search_msgs":
        matched_msgs = []
        since_date = datetime.datetime.utcnow() - datetime.timedelta(days=3)
        for g in chats:
            try:
                async for msg in userbot.iter_messages(g, limit=None):
                    msg_date = msg.date.replace(tzinfo=None) if msg.date.tzinfo else msg.date
                    if msg_date < since_date:
                        break
                    if msg.message and text.lower() in msg.message.lower():
                        link = f"https://t.me/{g.username}/{msg.id}" if getattr(g, "username", None) else None
                        matched_msgs.append((g.title, msg.message[:150], link))
            except Exception as e:
                print(f"Ошибка в {getattr(g,'title','unknown')}: {e}")
        if not matched_msgs:
            await message.answer("❌ За последние 3 дня объявлений не найдено")
        else:
            result_text = ""
            for g_title, snippet, link in matched_msgs[:20]:
                result_text += f"📌 {g_title}: {snippet}\n"
                if link:
                    result_text += f"🔗 {link}\n"
                result_text += "\n"
            await message.answer(result_text[:4000])
        state["mode"] = None

    elif mode == "global_search":
        matches = await global_search_all(userbot, text)
        if isinstance(matches, str):
            await message.answer(matches)
        elif not matches:
            await message.answer("❌ Ничего не найдено")
        else:
            result_text = ""
            for chat_title, snippet, link in matches[:30]:
                result_text += f"{chat_title}\n"
                if snippet:
                    result_text += f"{snippet}\n"
                if link:
                    result_text += f"🔗 {link}\n"
                result_text += "\n"
            await message.answer(result_text[:4000])
        state["mode"] = None

async def auto_search():
    dialogs = await userbot.get_dialogs()
    groups = [d.entity for d in dialogs if isinstance(d.entity, (types.Chat, types.Channel)) and 
              (not isinstance(d.entity, types.Channel) or d.entity.megagroup or d.entity.broadcast)]
    keywords = ["бишкек", "алматы", "логистика", "груз", "перевозка"]
    since_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    report = []
    for g in groups:
        try:
            async for msg in userbot.iter_messages(g, limit=100):
                msg_date = msg.date.replace(tzinfo=None) if msg.date.tzinfo else msg.date
                if msg_date < since_date:
                    break
                if msg.message and any(k in msg.message.lower() for k in keywords):
                    report.append(f"📌 {g.title}: {msg.message[:80]}")
                    break
        except Exception:
            continue
    if report:
        await bot.send_message(chat_id=5258340805,
                               text="📊 Автопоиск за сегодня:\n\n" + "\n".join(report[:20]))

import asyncio

async def main():
    await userbot.start()
    print("Userbot запущен")
    scheduler.add_job(auto_search, "cron", hour=10, minute=0)
    scheduler.start()
    print("Scheduler запущен")
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен пользователем")