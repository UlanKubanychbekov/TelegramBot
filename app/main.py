# app/main.py
import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from app.database import init_db

# --- Импорт роутеров ---
from app.api.EmployeeApi import router as employees_router
from app.api.RequestApi import router as requests_router
from app.api.SupplierApi import router as suppliers_router
from app.api.RequestSuggestionApi import router as suggestions_router
from app.api.TruckTypeApi import router as truck_types_router
from app.api.SpeedTypeApi import router as speed_types_router
from app.bot.handlers import register_handlers

# --- Логгер ---
logger = logging.getLogger("uvicorn.error")

# --- FastAPI приложение ---
app = FastAPI()

# --- Telegram bot ---
API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения!")

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
register_handlers(dp)

# --- API роуты ---
app.include_router(employees_router, prefix="/api", tags=["employees"])
app.include_router(requests_router, prefix="/api", tags=["requests"])
app.include_router(suppliers_router, prefix="/api", tags=["suppliers"])
app.include_router(suggestions_router, prefix="/api", tags=["suggestions"])
app.include_router(truck_types_router, prefix="/api", tags=["truck_types"])
app.include_router(speed_types_router, prefix="/api", tags=["speed_types"])

# --- Root ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application"}

# --- Глобальный обработчик ошибок ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred", "details": str(exc)},
    )

# --- Webhook endpoint ---
@app.post("/webhook")
async def telegram_webhook(update: dict):
    """Обработка входящих обновлений от Telegram"""
    try:
        tg_update = Update(**update)
        await dp.process_update(tg_update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Ошибка при обработке webhook: {e}")
        return {"ok": False, "error": str(e)}

# --- Ручка для установки webhook ---
@app.get("/set_webhook")
async def set_webhook():
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return {"ok": False, "error": "WEBHOOK_URL не задан"}
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook установлен на {webhook_url}")
        return {"ok": True, "message": f"Webhook установлен на {webhook_url}"}
    except Exception as e:
        logger.error(f"Не удалось установить webhook: {e}")
        return {"ok": False, "error": str(e)}

# --- Ручка для удаления webhook ---
@app.get("/delete_webhook")
async def delete_webhook():
    try:
        await bot.delete_webhook()
        logger.info("Webhook удалён")
        return {"ok": True, "message": "Webhook удалён"}
    except Exception as e:
        logger.error(f"Не удалось удалить webhook: {e}")
        return {"ok": False, "error": str(e)}

# --- Startup ---
@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("База данных инициализирована")

    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.set_webhook(webhook_url)
            logger.info(f"Webhook установлен автоматически на {webhook_url}")
        except Exception as e:
            logger.error(f"Не удалось установить webhook при старте: {e}")
    else:
        logger.warning("WEBHOOK_URL не задан — бот работать не будет!")

# --- Shutdown ---
@app.on_event("shutdown")
async def shutdown_event():
    try:
        await bot.delete_webhook()
        await bot.session.close()
        logger.info("Webhook удалён и сессия бота закрыта")
    except Exception as e:
        logger.error(f"Ошибка при остановке бота: {e}")
