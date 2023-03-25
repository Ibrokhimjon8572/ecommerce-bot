from django.conf import settings

import telebot
from telebot import types
from django.utils import translation
from django.utils.translation import gettext as _
from . import keyboards
import logging


BOT_TOKEN = getattr(settings, "BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


class Control:
    def handle_start(self, msg: types.Message):
        print("here")
        bot.send_message(msg.chat.id, _("hello_message"))