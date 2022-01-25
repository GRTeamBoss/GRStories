from email import message
import sqlite3

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.token import bot


def inline_info(call) -> None:
    print("[*] inline_info")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Profile", callback_data="/info profile"),
        InlineKeyboardButton("Account", callback_data="/info account"),
        InlineKeyboardButton("Statistics", callback_data="/info statistics"),
        InlineKeyboardButton("< Back", callback_data="/menu"),
    )
    bot.edit_message_text(chat_id=call.message.chat.id, text="Information about...", message_id=call.message.message_id, reply_markup=markup)


def account_info(call) -> None:
    print("[*] account_info")
    db = sqlite3.connect("bot.db")
    __profile = list(db.execute(f"select * from Profile where chat_id={call.message.chat.id}"))
    __followers_fields = list(db.execute(f"select count(author_id) from Follow where author_id={call.message.chat.id}"))[0]
    __follows_fields = list(db.execute(f"select count(follower_id) from Follow where follower_id={call.message.chat.id}"))[0]
    db.close()
    info = f"Nickname: {__profile[0][3]}\nFollows: {__follows_fields[0]}\nFollowers: {__followers_fields[0]}\nE-Mail: {__profile[0][5]}\nPhone: {__profile[0][6]}\nWeb-Site: {__profile[0][7]}\nDescription: {__profile[0][8]}"
    bot.edit_message_text(text=info, chat_id=call.message.chat.id, message_id=call.message.message_id)


def profile_info(call) -> None:
    print("[*] profile_info")
    db = sqlite3.connect("bot.db")
    __profile = list(db.execute(
        f"select * from Profile where chat_id={call.message.chat.id}"
    ))
    db.close()
    info = f"Name: {__profile[0][1]}\nLast name: {__profile[0][2]}\nNickname: {__profile[0][3]}\nCountry: {__profile[0][4]}\nE-Mail: {__profile[0][5]}\nPhone: {__profile[0][6]}\nWeb-Site: {__profile[0][7]}\nDescription: {__profile[0][8]}\nVisible: {'Yes' if __profile[0][10]==1 else 'No'}\nPopular: {'Yes' if __profile[0][11]==1 else 'No'}"
    bot.edit_message_text(text=info, chat_id=call.message.chat.id, message_id=call.message.message_id)


def statistics_info(call) -> None:
    print("[*] statistics_info")
    db = sqlite3.connect("bot.db")
    __stories = list(db.execute(f"select count(id) from Stories where chat_id={call.message.chat.id}"))[0]
    __watch = list(db.execute(f"select count(Watch.nickname) from Watch, Stories where Stories.chat_id={call.message.chat.id} and Stories.id=Watch.id"))[0]
    db.close()
    if __stories:
        info = f"Stories: {__stories[0]}\nViews: {__watch[0]}"
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("< Back", callback_data="/menu"))
        bot.edit_message_text(text=info, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    else:
        bot.edit_message_text(text="Your not have a stories!", chat_id=call.message.chat.id, message_id=call.message.message_id)