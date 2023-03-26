import telebot

from telebot import types
from django.utils.translation import gettext as _
from product.models import Category
from order.models import OrderItem


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
    buttons.append(_("basket"))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*buttons, row_width=2)
    return markup


def products_menu(products: list[Category], lang):
    buttons = []
    for product in products:
        product_name = product.name_uz if lang == 'uz' else product.name_ru
        buttons.append(product_name)

    buttons.append(_("back"))
    buttons.append(_("basket"))
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


def basket_keyboard(items: list[OrderItem], lang):
    buttons = [
        types.InlineKeyboardButton(_("back"), callback_data="back"),
        types.InlineKeyboardButton(_("order"), callback_data="order"),
        types.InlineKeyboardButton(_("clear basket"), callback_data="clear"),
    ]
    for item in items:
        name = item.product.name_uz if lang == 'uz' else item.product.name_ru
        buttons.append(types.InlineKeyboardButton(
            _("delete %(name)s" % {"name": name}),
            callback_data=f"delete__{name}"
        ))

    markup = types.InlineKeyboardMarkup()
    markup.add(*buttons, row_width=1)
    return markup
