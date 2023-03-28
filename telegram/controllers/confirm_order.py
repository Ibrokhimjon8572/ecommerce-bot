from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class ConfirmOrderHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def generate_text(self):
        text = "Yangi buyurtma: \n" \
            f"Tel: {self.user.phone} \n\n"
        price = 0
        for item in self.order.order_items.all():
            text += f"{item.product.name_uz} -- {item.amount}\n"
            price += item.price * item.amount
        text += f"Umumiy: {price} so'm\n"
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

            # send order to admins group

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
        self.reply(_("confirm order"), keyboards.confirm_order())
