import sqlite3
from types import NoneType
from typing import Union, Tuple


# Message
def bot_default_commands(message) -> bool:
    print("[*] bot_commands")
    commands = ("/start", "/help", "/menu")
    if message.text.split()[0] in commands:
        return True
    return False


def user_default_commands(message) -> bool:
    print("[*] user_default_commands")
    commands = ("/settings", "/stories", "/follows", "/followers", "/actions", "/info")
    if message.text.split()[0] in commands:
        return True
    return False


def profile_registration_is_actual(message) -> Union[Tuple[bool, str], Tuple[bool, NoneType]]:
    print("[*] profile_registration_is_actual")
    __fields = ("chat_id","name", "last_name", "nickname", "country", "email", "phone", "website", "description", "image", "visible", "popular")
    db = sqlite3.connect("bot.db")
    __profile = list(db.execute(
        f"select * from Profile where chat_id={message.chat.id}"
    ))
    db.close()
    for num in range(len(__profile[0])):
        if __profile[0][num] == None:
            return True, __fields[num]
    return False, None


def profile_empty_fields(message) -> bool:
    print("[*] profile_empty_fields")
    db = sqlite3.connect("bot.db")
    __profile = list(db.execute(
        f"select * from Profile where chat_id={message.chat.id}"
    ))
    db.close()
    if __profile:
        for num in range(len(__profile[0])):
            if __profile[0][num] == None:
                return True
        return False
    else:
        return True


# Callback
def user_inline_commands(call) -> bool:
    print("[*] user_commands")
    commands = ("/statistics", "/settings", "/followers", "/follows", "/remove", "/delete", "/info")
    if call.data in commands:
        return True
    return False