from telegram.control import Control, Handler
from telebot import types
from order.models import Order
from django.utils import translation
from django.utils.translation import gettext as _


class GroupHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, cq: types.CallbackQuery, message_id=None):
        bot = self.control.bot
        if cq.data.startswith("confirm_"):
            order_id = cq.data[8:]
            order = Order.objects.get(id=order_id)
            order.status = 'accepted'
            order.save()
            bot.edit_message_reply_markup(
                chat_id=cq.message.chat.id, message_id=cq.message.id, reply_markup=types.InlineKeyboardMarkup())
            bot.edit_message_text(
                cq.message.text + "\nTasdiqlandi ✅", chat_id=cq.message.chat.id, message_id=cq.message.id)
            translation.activate(order.user.language)
            bot.send_message(order.user.user_id, _('confirmed'))
        elif cq.data.startswith("reject_"):
            order_id = cq.data[7:]
            order = Order.objects.get(id=order_id)
            order.status = 'cancelled'
            order.save()
            bot.edit_message_reply_markup(
                chat_id=cq.message.chat.id, message_id=cq.message.id, reply_markup=types.InlineKeyboardMarkup())
            bot.edit_message_text(
                cq.message.text + "\nBekor qilindi ❌", chat_id=cq.message.chat.id, message_id=cq.message.id)
            translation.activate(order.user.language)
            bot.send_message(order.user.user_id, _('cancelled'))
