from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError
import logging

from services.notifier import send_notification
from database.repository import clean_old_notifications
from config.settings import CLEANUP_INTERVAL_DAYS

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def setup_scheduler():
    scheduler.start()
    
    scheduler.add_job(clean_old_notifications, 'interval', days=CLEANUP_INTERVAL_DAYS)
    
    logger.info("Планировщик задач запущен")

def schedule_notification(user_id: int, text: str, notification_time, notification_id: int, job_id: str):
    scheduler.add_job(
        send_notification,
        'date',
        run_date=notification_time,
        args=[user_id, text, notification_id],
        id=job_id
    )
    
    logger.info(f"Запланировано уведомление {notification_id} для пользователя {user_id} на {notification_time}")

def cancel_notification(job_id: str) -> bool:
    try:
        scheduler.remove_job(job_id)
        logger.debug(f"Задача {job_id} удалена из планировщика")
        return True
    except JobLookupError:
        logger.warning(f"Задача {job_id} не найдена в планировщике")
        return False