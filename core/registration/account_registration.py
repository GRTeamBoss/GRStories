import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from core.token import bot
from core.filter import *


def registration(message) -> None:
    print("[*] registration")
    __name = message.from_user.first_name if message.from_user.first_name is not None else None
    __last_name = message.from_user.last_name if message.from_user.last_name is not None else None
    __username = message.from_user.username if message.from_user.username is not None else None
    db = sqlite3.connect("bot.db")
    db.execute(
        f"insert or ignore into User (chat_id, name, last_name, username) values ({message.chat.id}, '{__name}', '{__last_name}', '{__username}')"
    )
    db.commit()
    db.execute(
        f"insert or ignore into Profile values ({message.chat.id}, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0)"
    )
    db.commit()
    db.close()
    markup = ReplyKeyboardMarkup(True, True, row_width=1)
    markup.add(KeyboardButton("share phone number", True))
    bot.send_message(message.chat.id, "Please share phone or set phone with form:\n<b>/setphone [phone]</b>\n[*] REQUIRED", reply_markup=markup)


def set_phone(message) -> None:
    print("[*] set_phone")
    db = sqlite3.connect("bot.db")
    if message.contact is not None:
        db.execute(
            f"update User set phone='{message.contact.phone_number}' where chat_id={message.chat.id}"
        )
    else:
        db.execute(
            f"update User set phone='{message.text.split()[1]}' where chat_id={message.chat.id}"
        )
    db.commit()
    db.close()
    markup = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Now you should registrate own profile with command: <strong>/reg_profile</strong>!", reply_markup=markup)