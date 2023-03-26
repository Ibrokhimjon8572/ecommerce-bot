from django.conf import settings

from telebot import types
from .control import bot, Control


@bot.message_handler(commands=['start'])
def handle_start(msg: types.Message):
    control = Control(msg.from_user)
    if control.user.phone:
        control.show_main_menu()
    else:
        control.show_ask_phone()


@bot.message_handler(content_types=['contact'])
def handle_contact(msg: types.Message):
    control = Control(msg.from_user)
    control.handle_contact(msg.contact)
