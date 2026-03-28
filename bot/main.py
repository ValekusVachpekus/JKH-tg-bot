import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import ADMIN_ID, BOT_TOKEN
from bot.database import init_db
from bot.handlers import admin, employee, user
from bot.logging_config import setup_logging, get_logger

logger = get_logger(__name__)


async def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан в .env")
    if not ADMIN_ID:
        raise ValueError("ADMIN_ID не задан в .env")

    setup_logging()
    
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(user.router)
    dp.include_router(employee.router)
    dp.include_router(admin.router)

    logger.info("🚀 Бот запущен. Admin ID: %s", ADMIN_ID)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
