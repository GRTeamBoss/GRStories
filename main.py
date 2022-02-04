#!/usr/bin/env python
#-*- coding:utf-8 -*-

from core.function import *
from core.token import bot

@bot.message_handler(func=lambda message: message)
def bot_commands(message):
    Commands(message)

if __name__ == "__main__":
    bot.polling(non_stop=True)