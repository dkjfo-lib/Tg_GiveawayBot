import os


LOCAL = False
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL") % os.getenv("BOT_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")