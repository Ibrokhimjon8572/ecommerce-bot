from django.conf import settings

import telebot
from telebot import types
from django.utils import translation
from django.utils.translation import gettext as _
from . import keyboards
import logging
from .models import User, UserSession


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

    def handle_contact(self, contact: types.Contact):
        if self.user_session.state == "ask_phone":
            self.user.phone = contact.phone_number
            self.user.save()
        self.show_main_menu()

    def show_ask_phone(self):
        self.user_session.state = "ask_phone"
        self.user_session.save()
        self.reply(_("hello_message"), keyboards.send_phone())

    def show_main_menu(self):
        self.user_session = "main_menu"
        self.reply(_("main_menu"), keyboards.main_menu())

    def reply(self, text, markup):
        bot.send_message(self.user_id, text, reply_markup=markup)
