import logging
from aiogram import Bot
from config.settings import BOT_TOKEN

logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

async def send_notification(user_id: int, text: str, notification_id: int):
    try:
        await bot.send_message(
            user_id,
            f"🔔 <b>Напоминание!</b>\n\n{text}",
            parse_mode="HTML"
        )
        logger.info(f"Уведомление {notification_id} отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления {notification_id}: {e}")