from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _

from telegram.utils import *


class ConfirmOrderHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def generate_text(self):
        text = "Yangi buyurtma: \n" \
            f"Holat: <b>Kutilmoqda</b>\n" \
            f"Tel: {self.user.phone} \n\n" \
            f"Manzil: {get_address(self.user_session.lat, self.user_session.long)} \n\n"
        price = 0
        for item in self.order.order_items.all():
            text += f"{number_to_emoji(item.amount)} ✖️ {item.product.name_uz}: {format_number(item.amount*item.price)}so'm\n"
            price += item.price * item.amount
        text += f"\n\n<b>Izoh:</b> {self.user_session.comment}\n\n"
        text += f"<b>Jami:</b> {price} so'm"

        return text

    def handle(self, text, message_id=None):
        if text == _("yes"):
            self.user_session.state = 'main_menu'
            self.user_session.save()
            self.order.status = 'pending'
            self.order.save()
            self.reply(_("order_accepted"))

            self.reply_group(self.generate_text(),
                             keyboards.admin_order(self.order.id), self.user_session.lat, self.user_session.long)

            return
        if text == _("no"):
            self.user_session.state = 'basket'
            self.user_session.lat = None
            self.user_session.long = None
            self.user_session.save()
            return
        self.reply(_("unknown"))


class ConfirmOrderDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        text = ""
        address = get_address(self.user_session.lat, self.user_session.long)
        if address:
            text += _("address %(address)s") % {"address": address}
            text += "\n"
        text += generate_text(self.order.order_items.all(), self.user.language)
        text += "\n"
        text += _("comment %(comment)s") % {
            "comment": self.user_session.comment}
        text += "\n\n"
        text += _("confirm order")
        self.reply(text, keyboards.confirm_order())
