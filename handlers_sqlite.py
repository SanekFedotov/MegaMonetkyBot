
from telebot import types
import random
import time
from utils import is_bonus_available, time_until_next_bonus, get_level
from data_manager import get_user, save_user

ADMIN_ID = 1005206357
ali_links = [
    "https://s.click.aliexpress.com/e/_EuvlOOw",
    "https://s.click.aliexpress.com/e/_Ez4sm1Y",
    "https://s.click.aliexpress.com/e/_EwvedEO",
    "https://s.click.aliexpress.com/e/_ExbJCdg",
    "https://s.click.aliexpress.com/e/_EH9xpH8",
    "https://s.click.aliexpress.com/e/_ExGcViA",
    "https://s.click.aliexpress.com/e/_EzGKTP0",
    "https://s.click.aliexpress.com/e/_EQPSMX8"
]
binance_url = "https://www.binance.com/referral/mystery-box/2025-pizza-day/claim?ref=GRO_16987_D1ZR2"

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        chat_id = str(message.chat.id)
        user = get_user(chat_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Натиснути", "Мій рахунок", "Запросити друга", "Магазин", "Щоденна нагорода", "Грати")
        bot.send_message(chat_id, "Привіт у MegaMonetkyBot!", reply_markup=markup)

    @bot.message_handler(func=lambda m: True)
    def handler(message):
        chat_id = str(message.chat.id)
        user = get_user(chat_id)
        text = message.text
        if text == "Натиснути":
            user["clicks"] += 1
            user["balance"] += 1
            user["level"] = get_level(user["clicks"])
            save_user(user)
            bot.send_message(chat_id, f"Монетка +1! Баланс: {user['balance']} | Рівень: {user['level']}")
            if user["clicks"] % 5 == 0:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("AliExpress знижка", url=random.choice(ali_links)))
                markup.add(types.InlineKeyboardButton("Binance Box", url=binance_url))
                bot.send_message(chat_id, "Подарунок за активність!", reply_markup=markup)
        elif text == "Мій рахунок":
            msg = f"Монети: {user['balance']}\nКліки: {user['clicks']}\nРівень: {user['level']}\nРеферали: {user['referrals']}"
            bot.send_message(chat_id, msg)
        elif text == "Щоденна нагорода":
            if is_bonus_available(user["last_bonus"]):
                user["balance"] += 15
                user["last_bonus"] = time.time()
                save_user(user)
                bot.send_message(chat_id, "Ти отримав +15 монет!")
            else:
                bot.send_message(chat_id, f"Зачекай: {time_until_next_bonus(user['last_bonus'])}")
        elif text == "Грати":
            number = random.randint(1, 5)
            user["game_state"] = {"active": True, "number": number}
            save_user(user)
            bot.send_message(chat_id, "Вгадай число від 1 до 5. Напиши його:")
        elif user.get("game_state", {}).get("active"):
            try:
                guess = int(text)
                actual = user["game_state"]["number"]
                user["game_state"]["active"] = False
                if guess == actual:
                    user["balance"] += 20
                    bot.send_message(chat_id, "Точно! +20 монет!")
                else:
                    user["balance"] -= 5
                    bot.send_message(chat_id, f"Не вгадав. Було: {actual}. -5 монет.")
                save_user(user)
            except:
                bot.send_message(chat_id, "Введи число від 1 до 5.")
