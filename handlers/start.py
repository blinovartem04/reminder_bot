import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.first_name
    
    await message.answer(
        f"👋 Привет, <b>{user_name}!</b>\n\n"
        f"Отправь мне текстовое сообщение с тем, о чем тебе напомнить.\n\n"
        f"<b>Например:</b>\n"
        f"- <i>Через 17 минут позвонить Любимой</i>\n"
        f"- <i>В 18:30 встреча с другом</i>\n"
        f"- <i>Завтра в 10:00 отправить отчет</i>\n\n"
        f"Также доступна команда:\n"
        f"<b>/list</b> - покажет активные напоминания\n",
        parse_mode="HTML"
    )
    logger.info(f"Пользователь {message.from_user.id} ({user_name}) запустил бота")