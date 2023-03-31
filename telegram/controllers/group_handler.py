from telegram.control import Control, Handler
from telebot import types
from order.models import Order
from django.utils import translation
from django.utils.translation import gettext as _
import os

CLICK_TOKEN = os.getenv("CLICK_PROVIDER_TOKEN")
PAYME_TOKEN = os.getenv("PAYME_PROVIDER_TOKEN")


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
                cq.message.text.replace("Kutilmoqda", "Tasdiqlandi"), chat_id=cq.message.chat.id, message_id=cq.message.id, parse_mode='html')
            translation.activate(order.user.language)
            bot.send_message(order.user.user_id, _('confirmed'))
            prices = [types.LabeledPrice(_("order title"), order.amount()*100)]
            if order.payment_type == "click" and CLICK_TOKEN:
                token = CLICK_TOKEN
            elif order.payment_type == "payme" and PAYME_TOKEN:
                token = PAYME_TOKEN
            else:
                return
            bot.send_invoice(
                order.user.user_id,
                _("order title"),
                _("description"),
                f"{cq.message.id} {order_id}",
                provider_token=token,
                currency="UZS",
                prices=prices,
            )
        elif cq.data.startswith("reject_"):
            order_id = cq.data[7:]
            order = Order.objects.get(id=order_id)
            order.status = 'cancelled'
            order.save()
            bot.edit_message_reply_markup(
                chat_id=cq.message.chat.id, message_id=cq.message.id, reply_markup=types.InlineKeyboardMarkup())
            bot.edit_message_text(
                cq.message.text.replace("Kutilmoqda", "Bekor qilindi"), chat_id=cq.message.chat.id, message_id=cq.message.id, parse_mode='html')
            translation.activate(order.user.language)
            bot.send_message(order.user.user_id, _('cancelled'))
