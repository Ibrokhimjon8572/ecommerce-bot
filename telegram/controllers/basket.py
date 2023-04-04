from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
import logging
from order.models import OrderItem
from telebot import types
from telegram.utils import *


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
            id = text[8:]
            logging.error(id)
            self.order.order_items.get(id=id).delete()
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
