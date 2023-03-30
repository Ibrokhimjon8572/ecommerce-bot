from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class SendCommentHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, msg, message_id=None):
        if msg == _("back"):
            self.user_session.state = 'order'
            self.user_session.save()
            return
        self.user_session.comment = msg
        self.user_session.state = 'choose_payment'
        self.user_session.save()


class SendCommentDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("send comment"), keyboards.comment_keyboard())
