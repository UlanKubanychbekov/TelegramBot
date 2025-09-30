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
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not API_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("BOT_TOKEN или WEBHOOK_URL не задан")

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

# --- Root endpoint ---
@app.get("/")
async def root():
    return {"message": "FastAPI + Aiogram Webhook is running"}

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
    try:
        tg_update = Update(**update)
        await dp.process_update(tg_update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return {"ok": False, "error": str(e)}

# --- Startup event ---
@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("База данных инициализирована")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook установлен на {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Не удалось установить webhook: {e}")

# --- Shutdown event ---
@app.on_event("shutdown")
async def shutdown_event():
    try:
        await bot.delete_webhook()
        await bot.session.close()
        logger.info("Webhook удалён и сессия бота закрыта")
    except Exception as e:
        logger.error(f"Ошибка при остановке бота: {e}")
