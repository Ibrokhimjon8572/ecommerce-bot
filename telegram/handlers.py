from telebot import types
from .control import bot, Control, Handler, Displayer
from .controllers import get_handler, get_displayer


@bot.message_handler(commands=['start'])
def handle_start(msg: types.Message):
    control = Control(msg.from_user)
    get_handler(control).handle(msg.text)
    get_displayer(control).show()


@bot.message_handler(content_types=['contact'])
def handle_contact(msg: types.Message):
    control = Control(msg.from_user)
    get_handler(control).handle(msg.contact.phone_number)
    get_displayer(control).show()


@bot.message_handler(content_types=['text'])
def handle_text(msg: types.Message):
    control = Control(msg.from_user)
    get_handler(control).handle(msg.text)
    get_displayer(control).show()
