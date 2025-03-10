import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_NAME = "notifications.db"

CLEANUP_INTERVAL_DAYS = 1
OLD_NOTIFICATION_DAYS = 7