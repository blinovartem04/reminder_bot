import sqlite3
import logging
import datetime
from typing import List, Tuple, Optional

from config.settings import DB_NAME, OLD_NOTIFICATION_DAYS

logger = logging.getLogger(__name__)

def save_notification(user_id: int, text: str, notification_time: datetime.datetime, job_id: str) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO notifications (user_id, text, notification_time, job_id) VALUES (?, ?, ?, ?)",
        (user_id, text, notification_time, job_id)
    )
    
    notification_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    logger.debug(f"Сохранено уведомление {notification_id} для пользователя {user_id}")
    return notification_id

def get_user_notifications(user_id: int) -> List[Tuple]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, text, notification_time, job_id FROM notifications WHERE user_id = ? AND notification_time > datetime('now')",
        (user_id,)
    )
    
    notifications = cursor.fetchall()
    conn.close()
    
    return notifications

def get_job_id(notification_id: int) -> Optional[str]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT job_id FROM notifications WHERE id = ?", (notification_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result[0] if result else None

def delete_notification(notification_id: int) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    if deleted:
        logger.debug(f"Удалено уведомление {notification_id}")
    
    return deleted

def clean_old_notifications() -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(f"DELETE FROM notifications WHERE notification_time < datetime('now', '-{OLD_NOTIFICATION_DAYS} days')")
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    if deleted_count > 0:
        logger.info(f"Удалено {deleted_count} старых уведомлений")
    
    return deleted_count