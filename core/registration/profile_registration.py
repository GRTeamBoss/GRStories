import requests, sqlite3


from core.token import TOKEN, bot
from core.filter import *


def get_profile_empty_fields(message):
    print("[*] get_profile_empty_fields")
    __field_funcs = {
        "name": get_field_or_none,
        "last_name": get_field_or_none,
        "nickname": get_field_or_none,
        "country": get_field_or_none,
        "email": get_field_or_none,
        "phone": get_field_or_none,
        "website": get_field_or_none,
        "description": get_field_or_none,
        "image": get_avatar_image,
    }
    __get_field = profile_registration_is_actual(message)[1]
    __field_funcs[__get_field](message)


def edit_profile_fields(message, field):
    print("[*] edit_profile_fields")
    db = sqlite3.connect("bot.db")
    db.execute(
        f"update Profile set {field}=NULL where chat_id={message.chat.id}"
    )
    db.commit()
    db.close()
    get_profile_empty_fields(message)


def get_field_or_none(message):
    print("[*] get_field_or_none")
    __field = profile_registration_is_actual(message)
    bot.send_message(message.chat.id, f"Please input your {__field[1]}")


def set_field_or_none(message):
    print("[*] set_field_or_none")
    __field = profile_registration_is_actual(message)
    db = sqlite3.connect("bot.db")
    db.execute(
        f"update Profile set {__field[1]}='{message.text}' where chat_id={message.chat.id}"
    )
    db.commit()
    db.close()
    get_profile_empty_fields(message)


def get_avatar_image(message):
    print("[*] get_avatar_image")
    bot.send_message(message.chat.id, "Please send your avatar(only image) as file")


def set_avatar_image(message):
    print("[*] set_avatar_image")
    if message.content_type == "document" and message.document.mime_type.split("/")[0]=="image":
        file_image_info = bot.get_file(message.document.file_id)
        file = requests.get(f"https://api.telegram.org/file/bot{TOKEN}/{file_image_info.file_path}")
        db = sqlite3.connect("bot.db")
        db.execute(f"update Profile set image=x'{file.content.hex()}' where chat_id={message.chat.id}")
        db.commit()
        db.close()
        get_profile_empty_fields(message)
    else:
        bot.send_message(message.chat.id, "Invalid type, please send as <strong>file/image</strong>", reply_to_message_id=message.message_id)