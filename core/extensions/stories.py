import sqlite3

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.token import bot

def inline_stories_list(call) -> None:
    markup = InlineKeyboardMarkup(row_width=1)
    db = sqlite3.connect("bot.db")
    __stories_fields = list(db.execute(f"select * from Stories where chat_id={call.message.chat.id}"))
    db.close()
    for item in __stories_fields:
        markup.add(InlineKeyboardButton(f"{item[2]}:{item[3]}", callback_data=f"/stories_info {item[1]}"))
    markup.add(InlineKeyboardButton("< Back", callback_data="/menu"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Your <b>Stories</b>:", reply_markup=markup)


def stories_info(call) -> None:
    markup = InlineKeyboardMarkup(row_width=1)
    db = sqlite3.connect("bot.db")
    __stories_field = list(db.execute(f"select * from Stories where chat_id={call.message.chat.id} and id={call.data.split()[1]}"))
    __watch_field = list(db.execute(f"select count(comment), count(nickname) from Watch where id={call.data.split()[1]} and nickname is not NULL"))[0]
    db.close()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Views: {__watch_field[1]}\nComments: {__watch_field[0]}")
