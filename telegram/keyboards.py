import telebot

from telebot import types
from django.utils.translation import gettext as _


def send_phone():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text=_("send_phone_text"), request_contact=True))
    return markup
