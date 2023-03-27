from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class OrderHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, msg, message_id=None):
        if type(msg) == str and msg == _("back"):
            self.user_session.state = 'basket'
            self.user_session.state.save()
            return
        if type(msg) == str:
            self.reply(_("unknown"))
            return
        # TODO: handle location

class OrderDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("send location"), keyboards.send_location())
