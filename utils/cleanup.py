import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional

from database.repository import clean_old_notifications
from config.settings import OLD_NOTIFICATION_DAYS

logger = logging.getLogger(__name__)

async def run_cleanup():
    """
    Удаляет уведомления, срок которых истек более OLD_NOTIFICATION_DAYS дней назад.
    """
    try:
        deleted_count = clean_old_notifications()
        logger.info(f"Очистка завершена. Удалено {deleted_count} старых уведомлений.")
    except Exception as e:
        logger.error(f"Ошибка при очистке старых данных: {e}")

async def schedule_periodic_cleanup(interval_hours: int = 24):
    while True:
        await run_cleanup()
        await asyncio.sleep(interval_hours * 3600)

def get_next_cleanup_time(base_time: Optional[datetime] = None) -> datetime:
    if base_time is None:
        base_time = datetime.now()
    
    next_cleanup = base_time.replace(hour=3, minute=0, second=0, microsecond=0)
    
    if base_time >= next_cleanup:
        next_cleanup += timedelta(days=1)
    
    return next_cleanup

async def schedule_smart_cleanup():
    next_cleanup = get_next_cleanup_time()
    now = datetime.now()
    
    wait_seconds = (next_cleanup - now).total_seconds()
    
    logger.info(f"Следующая очистка запланирована на {next_cleanup}")
    await asyncio.sleep(wait_seconds)
    
    await schedule_periodic_cleanup()