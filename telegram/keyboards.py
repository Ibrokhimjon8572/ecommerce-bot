import telebot

from telebot import types
from django.utils.translation import gettext as _
from product.models import Category


def send_phone():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(
        text=_("send_phone_text"), request_contact=True))
    return markup


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(
        text=_("orders")
    ))
    markup.add(types.KeyboardButton(
        text=_("basket")
    ))
    return markup


def categories_menu(categories: list[Category], lang):
    buttons = []
    for category in categories:
        category_name = category.name_uz if lang == 'uz' else category.name_ru
        buttons.append(types.KeyboardButton(category_name))

    buttons.append(_("back"))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons, row_width=2)
    return markup


def products_menu(products: list[Category], lang):
    buttons = []
    for product in products:
        product_name = product.name_uz if lang == 'uz' else product.name_ru
        buttons.append(types.KeyboardButton(product_name))

    buttons.append(_("back"))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons, row_width=2)
    return markup


def choose_keyboard():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton(_("basket")))
    markup.row(types.KeyboardButton(_("back")))
    return markup


def amount_keyboard(amount):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("-", callback_data="-"),
        types.InlineKeyboardButton(f"{amount}", callback_data="show"),
        types.InlineKeyboardButton("+", callback_data="+"),
    )
    markup.add(
        types.InlineKeyboardButton(
            _("add to basket"), callback_data='add_to_basket')
    )
    return markup
