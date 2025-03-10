import datetime
import logging
import uuid
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.repository import save_notification, get_user_notifications, delete_notification, get_job_id
from services.scheduler import schedule_notification, cancel_notification
from keyboards.inline import get_notifications_keyboard
from nlp.time_parser import TimeParser
from nlp.intent_recognizer import IntentRecognizer

logger = logging.getLogger(__name__)
router = Router()

time_parser = TimeParser()
intent_recognizer = IntentRecognizer()

@router.message(Command("list"))
async def cmd_list(message: Message):
    await show_notifications_list(message)

@router.callback_query(F.data.startswith("delete_"))
async def process_delete_callback(callback: CallbackQuery):
    notification_id = int(callback.data.split("_")[1])
    
    job_id = get_job_id(notification_id)
    
    if job_id and delete_notification(notification_id):
        cancel_notification(job_id)
        
        await callback.answer("Уведомление удалено!")
        logger.info(f"Пользователь {callback.from_user.id} удалил уведомление {notification_id}")
        
        await update_notifications_list(callback)
    else:
        await callback.answer("Ошибка при удалении уведомления.")
        logger.error(f"Ошибка при удалении уведомления {notification_id}")

@router.message()
async def process_natural_language(message: Message):
    intent = intent_recognizer.recognize_intent(message.text)
    
    if not intent:
        await message.answer(
            f"Произошла ошибка при обработке запроса. Пожалуйста, попробуй cоставить по другому.\n\n"
            f"<b>Например:</b>\n"
            f"- <i>Через 17 минут позвонить Любимой</i>\n"
            f"- <i>В 18:30 встреча с другом</i>\n"
            f"- <i>Завтра в 10:00 отправить отчет</i>\n\n"
            f"Также доступна команда:\n"
            f"<b>/list</b> - покажет активные напоминания\n",
            parse_mode="HTML"
        )
        return
    
    if intent['intent'] == 'create_reminder':
        parsed_data = time_parser.parse_time(intent['text'])
        
        if parsed_data:
            notification_time, notification_text = parsed_data
            
            if notification_time <= datetime.datetime.now():
                await message.answer(
                    "⚠️ Я не могу создать напоминание на прошедшее время."
                )
                return
            
            await create_notification(message, notification_text, notification_time)
        else:
            await message.answer(
                "⏰ Не смог определить время. "
                "Пожалуйста, укажите время более точно!"
            )
    
    elif intent['intent'] == 'list_reminders':
        await show_notifications_list(message)
    
    elif intent['intent'] == 'cancel_reminder':
        await show_notifications_list(message, "Выберите напоминание для удаления:")

async def create_notification(message: Message, notification_text: str, notification_time: datetime.datetime):
    job_id = f"notification_{message.from_user.id}_{str(uuid.uuid4())[:8]}"
    
    notification_id = save_notification(
        message.from_user.id,
        notification_text,
        notification_time,
        job_id
    )
    
    schedule_notification(
        message.from_user.id,
        notification_text,
        notification_time,
        notification_id,
        job_id
    )
    
    time_delta = notification_time - datetime.datetime.now()
    minutes = int(time_delta.total_seconds() / 60)
    hours = minutes // 60
    minutes = minutes % 60
    
    time_str = notification_time.strftime("%d.%m.%Y %H:%M:%S")
    
    if hours > 0 and minutes > 0:
        time_left = f"через {hours} ч {minutes} мин"
    elif hours > 0:
        time_left = f"через {hours} ч"
    else:
        time_left = f"через {minutes} мин"
    
    await message.answer(
        f"✅ Напоминание создано!\n\n"
        f"📝 <b>{notification_text}</b>\n"
        f"⏰ {time_str} ({time_left})",
        parse_mode="HTML"
    )
    
    logger.info(f"Пользователь {message.from_user.id} создал уведомление {notification_id} на {time_str}")

async def show_notifications_list(message: Message, header_text: str = None):
    notifications = get_user_notifications(message.from_user.id)
    
    if not notifications:
        await message.answer("У вас нет активных напоминаний.")
        logger.debug(f"Пользователь {message.from_user.id} запросил список напоминаний (пусто)")
        return
    
    text = header_text or "📋 <b>Ваши активные напоминания:</b>\n\n"
    
    for idx, (notification_id, notification_text, notification_time, _) in enumerate(notifications, start=1):
        time_obj = datetime.datetime.fromisoformat(notification_time)
        time_str = time_obj.strftime("%d.%m.%Y %H:%M")

        time_delta = time_obj - datetime.datetime.now()
        minutes = int(time_delta.total_seconds() / 60)
        hours = minutes // 60
        minutes = minutes % 60
        
        if hours > 0 and minutes > 0:
            time_left = f"через {hours} ч {minutes} мин"
        elif hours > 0:
            time_left = f"через {hours} ч"
        else:
            time_left = f"через {minutes} мин"
        
        text += f"{idx}. <b>{notification_text}</b>\n⏰ {time_str} ({time_left})\n\n"
    
    keyboard = get_notifications_keyboard(notifications)
    
    await message.answer(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    logger.debug(f"Пользователь {message.from_user.id} просмотрел список напоминаний ({len(notifications)} шт.)")

async def update_notifications_list(callback: CallbackQuery):
    notifications = get_user_notifications(callback.from_user.id)
    
    if not notifications:
        await callback.message.edit_text("У вас нет активных напоминаний.")
        return
    
    text = "📋 <b>Ваши активные напоминания:</b>\n\n"
    
    for idx, (notification_id, notification_text, notification_time, _) in enumerate(notifications, start=1):
        time_obj = datetime.datetime.fromisoformat(notification_time)
        time_str = time_obj.strftime("%d.%m.%Y %H:%M")

        time_delta = time_obj - datetime.datetime.now()
        minutes = int(time_delta.total_seconds() / 60)
        hours = minutes // 60
        minutes = minutes % 60
        
        if hours > 0 and minutes > 0:
            time_left = f"через {hours} ч {minutes} мин"
        elif hours > 0:
            time_left = f"через {hours} ч"
        else:
            time_left = f"через {minutes} мин"
        
        text += f"{idx}. <b>{notification_text}</b>\n⏰ {time_str} ({time_left})\n\n"
    
    keyboard = get_notifications_keyboard(notifications)
    
    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )