from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import logging
from order.models import OrderItem
from telebot import types
from django.db.models import Q


def generate_text(items, lang):
    text = _("products:\n")
    price = 0
    for item in items:
        name = item.product.name_uz if lang == 'uz' else item.product.name_ru
        text += _("%(name)s x %(amount)d \n" %
                  {"name": name, "amount": item.amount})
        price += item.price * item.amount
    text += _("total: %(price)d so'm" % {"price": price})
    return text


class BasketHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == "back":
            self.user_session.state = 'main_menu'
            self.user_session.save()
            return
        if text == "order":
            self.user_session.state = 'order'
            self.user_session.save()
            return
        if text == "clear":
            self.reply(_("basked cleared"))
            self.user_session.state = 'main_menu'
            self.user_session.save()
            for order_item in self.order.order_items.all():
                order_item: OrderItem
                order_item.delete()
            return
        if text.startswith("delete_"):
            product_name = text[8:]
            logging.error(product_name)
            self.order.order_items.get(
                Q(product__name_uz=product_name) | Q(product__name_ru=product_name)).delete()
        order_items = self.order.order_items.all()
        if len(order_items):
            self.edit_markup(message_id, keyboards.basket_keyboard(
                order_items, self.user.language), generate_text(order_items, self.user.language))
        else:
            self.reply(_("empty basket"))
            self.user_session.state = 'main_menu'
            self.user_session.save()


class BasketDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        order_items = self.order.order_items.all()
        logging.error(order_items)
        text = generate_text(order_items, self.user.language)
        self.reply(_("basket"), types.ReplyKeyboardRemove())
        if len(order_items):
            self.reply(text, keyboards.basket_keyboard(
                order_items, self.user.language))
        else:
            self.reply(_("empty basket"))
            self.user_session.state = 'main_menu'
            self.user_session.save()
            self.reply(_("main_menu"), keyboards.main_menu())
