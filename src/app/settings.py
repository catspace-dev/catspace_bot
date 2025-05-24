import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMINS = set(map(int, os.getenv("ADMINS", "0").split(",")))
ALLOWED_CHATS = set(map(int, os.getenv("ADMINS", "0").split(",")))
