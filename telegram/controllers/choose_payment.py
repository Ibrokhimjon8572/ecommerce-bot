from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class ChoosePaymentHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == _("back"):
            self.user_session.state = 'send_comment'
            self.user_session.save()
            return
        if text == _("payme"):
            self.user_session.state = 'confirm_order'
            self.user_session.payment_method = text
            self.user_session.save()
        if text == _("click"):
            self.user_session.state = 'confirm_order'
            self.user_session.payment_method = text
            self.user_session.save()
        if text == _("cash"):
            self.user_session.state = 'confirm_order'
            self.user_session.payment_method = text
            self.user_session.save()
        if text == _("terminal"):
            self.user_session.state = 'confirm_order'
            self.user_session.payment_method = text
            self.user_session.save()


class ChoosePaymentDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("ask payment"), keyboards.select_payment())
