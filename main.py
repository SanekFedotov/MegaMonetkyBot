
from telebot import TeleBot
from handlers_sqlite import register_handlers
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(TOKEN)

register_handlers(bot)

bot.polling()
