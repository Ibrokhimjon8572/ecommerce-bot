from telegram.control import Handler, Control, ADMIN_GROUP
from telebot import types
from order.models import Order
from django.utils.translation import gettext as _


class PaymentHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def valid(self, payment: types.PreCheckoutQuery, message_id=None):
        message_id, order_id = payment.invoice_payload.split()
        order = Order.objects.get(id=order_id)
        return order.status == "accepted"

    def handle(self, payment: types.SuccessfulPayment, message_id=None):
        message_id, order_id = payment.invoice_payload.split()
        order = Order.objects.get(id=order_id)
        order.status = 'paid'
        order.save()

        self.control.bot.send_message(
            ADMIN_GROUP, "To'landi", reply_to_message_id=message_id)

        self.reply(_("payment success"))
