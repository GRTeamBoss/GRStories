from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.token import bot
from core.filter import *


def usage(message) -> None:
    print("[*] usage")
    info = str("/menu\n/setphone [phone]\n/reg_profile")
    bot.send_message(message.chat.id, info)


def menu(call=False, message=False) -> None:
    print("[*] menu")
    if call:
        print("[*] menu -> call")
        if profile_registration_is_actual(call.message)[0] is False:
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("Actions", callback_data="/actions"),
                InlineKeyboardButton("Followers", callback_data="/followers"),
                InlineKeyboardButton("Follows", callback_data="/follows"),
                InlineKeyboardButton("Settings", callback_data="/settings"),
                InlineKeyboardButton("Stories", callback_data="/stories"),
                InlineKeyboardButton("Information", callback_data="/info"),
            )
            bot.edit_message_text("Menu:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.edit_message_text("Now you should registrate own profile with command: <strong>/reg_profile</strong>!", call.message.chat.id, call.message.message_id)
    elif message:
        print("[*] menu -> message")
        if profile_registration_is_actual(message)[0] is False:
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("Actions", callback_data="/actions"),
                InlineKeyboardButton("Followers", callback_data="/followers"),
                InlineKeyboardButton("Follows", callback_data="/follows"),
                InlineKeyboardButton("Settings", callback_data="/settings"),
                InlineKeyboardButton("Stories", callback_data="/stories"),
                InlineKeyboardButton("Information", callback_data="/info"),
            )
            bot.send_message(message.chat.id, "Menu:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Now you should registrate own profile with command: <strong>/reg_profile</strong>!")