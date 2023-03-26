from django.conf import settings

import telebot
from telebot import types
from django.utils import translation
from django.utils.translation import gettext as _
from . import keyboards
from .models import User, UserSession
from abc import ABC, abstractmethod


BOT_TOKEN = getattr(settings, "BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


class Control:
    def __init__(self, tg_user: types.User):
        self.user_id = tg_user.id
        self.user, _ = User.objects.get_or_create(user_id=tg_user.id, defaults={
            "name": f"{tg_user.first_name} {tg_user.last_name or ''}",
            "username": tg_user.username,
        })
        self.user_session, _ = UserSession.objects.get_or_create(user=self.user, defaults={
            "state": "ask_phone"
        })
        translation.activate(self.user.language)

    def reply(self, text, markup=None):
        bot.send_message(self.user_id, text, reply_markup=markup)


class Handler(ABC):
    def __init__(self, control: Control):
        self.user = control.user
        self.user_session = control.user_session
        self.reply = control.reply

    @abstractmethod
    def handle(self, text):
        pass


class Displayer:
    def __init__(self, control: Control):
        self.user = control.user
        self.user_session = control.user_session
        self.reply = control.reply

    @abstractmethod
    def show(self):
        pass
