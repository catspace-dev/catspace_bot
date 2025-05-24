import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMINS = map(int, os.getenv("ADMINS", "0").split(","))
