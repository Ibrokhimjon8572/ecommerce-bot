from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
from telebot import types


class OrderHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, msg, message_id=None):
        if msg == _("back"):
            self.user_session.state = 'basket'
            self.user_session.save()
            return
        if msg == _("skip"):
            self.user_session.state = 'send_comment'
            self.user_session.lat = None
            self.user_session.long = None
            self.user_session.save()
            return
        if msg == _("my addresses"):
            self.user_session.state = 'select_from_addresses'
            self.user_session.save()
            return
        if type(msg) == str:
            self.reply(_("unknown"))
            return
        if type(msg) == types.Location:
            self.user_session.state = 'send_comment'
            self.user_session.lat = msg.latitude
            self.user_session.long = msg.longitude
            self.user_session.save()


class OrderDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("send location"), keyboards.send_location())
