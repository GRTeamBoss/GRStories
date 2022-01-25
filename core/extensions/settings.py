import sqlite3

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.token import bot


def settings(call) -> None:
    print("[*] settings")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Profile", callback_data="/edit profile"),
        InlineKeyboardButton("Visible", callback_data="/edit visible"),
        InlineKeyboardButton("Delete account", callback_data="/delete"),
        InlineKeyboardButton("< Back", callback_data="/menu")
    )
    bot.edit_message_text(text="Settings:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def profile_settings(call) -> None:
    print("[*] profile_settings")
    __fields = ("chat_id","name", "last_name", "nickname", "country", "email", "phone", "web-site", "description", "image", "visible", "popular")
    db = sqlite3.connect("bot.db")
    __profile = list(db.execute(f"select * from Profile where chat_id={call.message.chat.id}"))
    db.close()
    markup = InlineKeyboardMarkup(row_width=1)
    for field in __profile[0]:
        markup.add(InlineKeyboardButton(field, callback_data=f"/profile_edit {__fields[__profile[0].index(field)]}"))
    markup.add(InlineKeyboardButton("< Back", callback_data="/menu"))
    bot.edit_message_text(text="What you wanna change?", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def visible_settings(call) -> None:
    print("[*] visible_settings")
    markup = InlineKeyboardMarkup(row_width=1)
    db = sqlite3.connect("bot.db")
    __profile_fields = list(db.execute(f"select * from Profile where chat_id={call.message.chat.id}"))[0]
    db.close()
    __profile_visible_status = "enable" if __profile_fields[10]==0 else "disable"
    markup.add(
        InlineKeyboardButton(f"Visible {'ON' if __profile_visible_status=='enable' else 'OFF'}", callback_data=f"/visible {__profile_visible_status}"),
        InlineKeyboardButton("< Back", callback_data="/settings")
    )
    bot.edit_message_text(f"Your account is {'Invisible' if __profile_visible_status=='enable' else 'Visible'}", call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def delete(call) -> None:
    print("[*] delete")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Delete account!", callback_data=f"/delete account"),
        InlineKeyboardButton("< Back", callback_data="/menu")
    )
    bot.edit_message_text(text="Your really wanna delete account?!", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def delete_account(call) -> None:
    print("[*] delete_account")
    db = sqlite3.connect("bot.db")
    db.execute(
        f"delete from User, Stories, Follow, Profile where chat_id={call.message.chat.id}"
    )
    db.commit()
    db.close()
    bot.edit_message_text(text="Account deleted!", chat_id=call.message.chat.id, message_id=call.message.message_id)