from telegram.control import Handler, Control, ADMIN_GROUP
from telebot import types

from django.utils.translation import gettext as _


class PaymentHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, payment: types.SuccessfulPayment, message_id=None):
        message_id = payment.invoice_payload

        self.control.bot.send_message(
            ADMIN_GROUP, "To'landi", reply_to_message_id=message_id)

        self.reply(_("payment success"))
