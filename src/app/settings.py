import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMINS = set(map(int, os.getenv("ADMINS", "0").split(",")))
ALLOWED_CHATS = set(map(int, os.getenv("ALLOWED_CHATS", "0").split(",")))
SENTRY_DSN = os.getenv("SENTRY_DSN")
