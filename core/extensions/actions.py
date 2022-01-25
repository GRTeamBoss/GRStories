import sqlite3

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.token import bot
from core.filter import *


def inline_actions_list(call) -> None:
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("") # TODO
    )

# Message
def post_stories(message) -> None:
    print("[*] post_stories")
    __stories_type = message.content_type
    if message.text:
        __stories_data = message.text
    elif message.audio:
        __stories_data = message.audio
    elif message.photo:
        __stories_data = message.photo
    elif message.video:
        __stories_data = message.video
    elif message.voice:
        __stories_data = message.voice
    db = sqlite3.connect("bot.db")
    db.execute(f"update Stories set type='{__stories_type}', data='{__stories_data}' where chat_id={message.chat.id}")
    db.commit()
    db.close()
    bot.send_message("Stories form is valid!")


# Callback
def new_stories(call) -> None:
    print("[*] new_stories")
    db = sqlite3.connect("bot.db")
    db.execute(f"insert into Stories (chat_id, id, date) values ({call.message.chat.id}, (select (count(id)+1) from Stories where chat_id={call.message.chat.id}), '{call.message.date}')")
    db.commit()
    db.close()
    bot.send_message("Please send something for stories; text, image, video or voice")


def remove(call) -> None:
    print("[*] remove")
    db = sqlite3.connect("bot.db")
    __stories = list(db.execute(
        f"select * from Stories where chat_id={call.message.chat.id}"
    ))
    db.close()
    markup = InlineKeyboardMarkup(row_width=1)
    if __stories:
        for field in __stories:
            markup.add(InlineKeyboardButton(f"date: {field[3]} type: {field[2]}", callback_data=f"/remove {field[1]}"))
        markup.add(InlineKeyboardButton("< Back", callback_data="/menu"))
        bot.edit_message_text(text="Your stories:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("< Back", callback_data="/menu"))
        bot.edit_message_text(text="Your not have a stories!", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def remove_stories(call) -> None:
    print("[*] remove_stories")
    db = sqlite3.connect("bot.db")
    db.execute(
        f"delete from Stories, Watch where id={call.data.split()[1]}"
    )
    db.commit()
    db.close()
    remove(call)


def stories_all(call) -> None:
    print("[*] stories_all")
    __stories_type = {
        "text": lambda message, fields: bot.send_message(chat_id=message.chat.id, text=fields[1]),
        "photo": lambda message, fields: bot.send_photo(chat_id=message.chat.id, photo=fields[1]),
        "voice": lambda message, fields: bot.send_voice(chat_id=message.chat.id, voice=fields[1]),
        "video": lambda message, fields: bot.send_video(chat_id=message.chat.id, data=fields[1]),
        "audio": lambda message, fields: bot.send_audio(chat_id=message.chat.id, audio=fields[1]),
    }
    db = sqlite3.connect("bot.db")
    __stories_fields = list(db.execute(f"select Stories.id, Stories.data, Stories.type from Stories, Watch where not EXISTS (select id from Watch where nickname=(select nickname from Profile where chat_id={call.message.chat.id}))").fetchone())[0]
    __profile_fields = list(db.execute(f"select nickname from Profile where chat_id={call.message.chat.id}"))[0]
    db.execute(f"insert into Watch (id, nickname) values ({__stories_fields[0]}, {__profile_fields[0]})")
    db.commit()
    db.close()
    __stories_type[__stories_fields[2]](call.message, __stories_fields)


def stories_of_account(call) -> None:
    print("[*] stories_of_account")
    __account = call.data.split()[1]
    __stories_type = {
        "text": lambda message, fields: bot.send_message(chat_id=message.chat.id, text=fields[1]),
        "photo": lambda message, fields: bot.send_photo(chat_id=message.chat.id, photo=fields[1]),
        "voice": lambda message, fields: bot.send_voice(chat_id=message.chat.id, voice=fields[1]),
        "video": lambda message, fields: bot.send_video(chat_id=message.chat.id, data=fields[1]),
        "audio": lambda message, fields: bot.send_audio(chat_id=message.chat.id, audio=fields[1]),
    }
    db = sqlite3.connect("bot.db")
    __stories_fields = list(db.execute(f"select Stories.id, Stories.data, Stories.type from Stories, Watch where not EXISTS (select id from Watch where nickname=(select nickname from Profile where chat_id={call.message.chat.id})) and Stories.chat_id={__account}").fetchone())[0]
    __profile_fields = list(db.execute(f"select nickname from Profile where chat_id={call.message.chat.id}"))[0]
    db.execute(f"insert into Watch (id, nickname) values ({__stories_fields[0]}, {__profile_fields[0]})")
    db.commit()
    db.close()
    __stories_type[__stories_fields[2]](call.message, __stories_fields)