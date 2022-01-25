import sqlite3

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.token import bot


def followers(call) -> None:
    print("[*] followers")
    db = sqlite3.connect("bot.db")
    __follower = list(db.execute(f"select chat_id from Follow where nickname=(select nickname from Profile where chat_id={call.message.chat.id})"))[:10]
    db.close()
    markup = InlineKeyboardMarkup(row_width=1)
    for item in __follower:
        markup.add(InlineKeyboardButton(item[0], callback_data=f"/account {item[0]}"))
    markup.add(InlineKeyboardButton("< Back", callback_data="/menu"))
    bot.edit_message_text(text=f"Your followers:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def follows(call) -> None:
    print("[*] follows")
    db = sqlite3.connect("bot.db")
    __follow = list(db.execute(
        f"select nickname from Follow where chat_id={call.message.chat.id}"
    ))
    db.close()
    markup = InlineKeyboardMarkup(row_width=1)
    for item in __follow:
        markup.add(InlineKeyboardButton(item[0], callback_data=f"/account {item[0]}"))
    markup.add(InlineKeyboardButton("< Back", callback_data="/menu"))
    bot.edit_message_text(text=f"Your follows:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)