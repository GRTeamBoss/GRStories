#!/usr/bin/env python
#-*- coding:utf-8 -*-

from core.registration.account_registration import *
from core.registration.profile_registration import *
from core.extensions.actions import *
from core.extensions.bot_commands import *
from core.extensions.follow import *
from core.extensions.info import *
from core.extensions.settings import *
from core.extensions.stories import *
from core.filter import *
from core.telegram import *
from core.token import bot


# Message
@bot.message_handler(func=lambda message: message)
def bot_command_execute(message):
    if bot_default_commands(message) is True:
        funcs = {
            "/start": registration,
            "/help": usage,
            "/menu": menu,
        }
        funcs[message.text](message=message)
    elif message.content_type=="contact" or message.text.startswith("/setphone ") and len(message.text.split())==2:
        set_phone(message)
    elif message.text=="/reg_profile" and profile_empty_fields(message) is True:
        get_profile_empty_fields(message)
    elif profile_registration_is_actual(message)[0] is True:
        __field_funcs = {
            "name": set_field_or_none,
            "last_name": set_field_or_none,
            "nickname": set_field_or_none,
            "country": set_field_or_none,
            "email": set_field_or_none,
            "phone": set_field_or_none,
            "website": set_field_or_none,
            "description": set_field_or_none,
            "image": set_avatar_image,
        }
        __set_field = profile_registration_is_actual(message)[1]
        __field_funcs[__set_field](message)


# Callback
@bot.callback_query_handler(func=lambda call: call)
def user_inline_command_execute(call):
    if user_inline_commands(call) is True:
        funcs = {
            "/statistics": statistics_info,
            "/settings": settings,
            "/followers": followers,
            "/follows": follows,
            "/remove": remove,
            "/delete": delete,
            "/info": inline_info,
            "/stories_info": inline_stories_list,
        }
        funcs[call.data](call)
    elif len(call.data.split())==2:
        if call.data.split()[0]=="/delete":
            delete_account(call)
        elif call.data.split()[0]=="/edit":
            edit_funcs = {
                "profile": profile_settings,
                "visible": visible_settings,
            }
            edit_funcs[call.data.split[1]](call)
        elif call.data.split()[0]=="/profile_edit":
            edit_profile_fields(call.message, call.data.split()[1])
        elif call.data.split()[0]=="/remove":
            remove_stories(call)
        elif call.data.split()[0]=="/stories_info":
            stories_info(call)
        elif call.data.split()[0]=="/info":
            info_funcs = {
                "profile": profile_info,
                "account": account_info,
                "statistics": statistics_info,
            }
            info_funcs[call.data.split()[1]](call)


if __name__ == "__main__":
    bot.polling(non_stop=True, timeout=0)