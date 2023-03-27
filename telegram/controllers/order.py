from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
from telebot import types


class OrderHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, msg, message_id=None):
        if type(msg) == str and msg == _("back"):
            self.user_session.state = 'basket'
            self.user_session.save()
            return
        if type(msg) == str:
            self.reply(_("unknown"))
            return
        if type(msg) == types.Location:
            self.user_session.state = 'main_menu'
            self.user_session.save()
            self.reply(_("order_accepted"))
            self.order.status = 'pending'

            # TODO: send order to admin group


class OrderDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("send location"), keyboards.send_location())
