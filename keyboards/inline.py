from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Tuple

def get_notifications_keyboard(notifications: List[Tuple]):
    keyboard = InlineKeyboardBuilder()
    
    for idx, (notification_id, _, _, _) in enumerate(notifications, start=1):
        keyboard.button(
            text=f"❌ Удалить #{idx}", 
            callback_data=f"delete_{notification_id}"
        )
    
    keyboard.adjust(1)
    
    return keyboard.as_markup()