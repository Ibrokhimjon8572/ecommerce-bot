from django.conf import settings

import telebot
from telebot import types
from django.utils import translation
from django.utils.translation import gettext as _
from .models import User, UserSession
from order.models import Order
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
            "state": "start"
        })
        self.url = "/".join(bot.get_webhook_info().url.split("/")[:-2])
        self.order, _ = Order.objects.get_or_create(
            user=self.user, status='created')
        translation.activate(self.user.language)

    def reply(self, text, markup=None):
        bot.send_message(self.user_id, text, reply_markup=markup)

    def reply_image(self, image, caption, markup=None):
        bot.send_photo(self.user_id, image,
                       caption=caption, reply_markup=markup)

    def edit_markup(self, message_id, markup, text=None):
        bot.edit_message_reply_markup(
            self.user_id, message_id, reply_markup=markup)
        if text is not None:
            bot.edit_message_text(text, self.user_id, message_id)


class Handler(ABC):
    def __init__(self, control: Control):
        self.user = control.user
        self.user_session = control.user_session
        self.reply = control.reply
        self.reply_image = control.reply_image
        self.edit_markup = control.edit_markup
        self.order = control.order
        self.control = control

    @abstractmethod
    def handle(self, text, message_id=None):
        pass


class Displayer:
    def __init__(self, control: Control):
        self.user = control.user
        self.user_session = control.user_session
        self.reply = control.reply
        self.reply_image = control.reply_image
        self.order = control.order
        self.control = control
        self.base_url = control.url

    @abstractmethod
    def show(self):
        pass
