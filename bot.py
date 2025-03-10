import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import BOT_TOKEN
from database.models import init_db
from config.settings import DB_NAME
from services.scheduler import setup_scheduler
from handlers import notifications, start
from middlewares.throttling import ThrottlingMiddleware
from utils.cleanup import schedule_smart_cleanup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.message.middleware(ThrottlingMiddleware(rate_limit=0.7))
    
    dp.include_router(start.router)
    dp.include_router(notifications.router)
    
    init_db(DB_NAME)
    
    setup_scheduler()
    
    asyncio.create_task(schedule_smart_cleanup())
    
    logger.info("Бот запущен с поддержкой естественного языка")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")