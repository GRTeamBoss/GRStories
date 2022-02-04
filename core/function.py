import json, subprocess

from core.token import bot


class Commands:

    def __init__(self, message) -> None:
        self.message = message
        match self.message.text:
            case "/start":
                self.start
            case "/help":
                self.usage
            case "/menu":
                pass
            case "/faq":
                self.faq


    
    def start(self):
        info = "Hello, I am GRStories bot for posting your stories, videos, audio, texts. You can also post anonymously and no one will do not know who posted unless you not add your tag or name."
        bot.send_message(chat_id=self.message.chat.id, text=info)


    @staticmethod
    def usage(self):
        info = "commands----\n/start\n/help <-- \n/menu\n/faq"
        bot.send_message(chat_id=self.message.chat.id, text=info)


    @staticmethod
    def faq(self):
        info = "You will get the status of a star person when the number of your subscribers is greater than or equal to 100,000"
        bot.send_message(chat_id=self.message.chat.id, text=info)