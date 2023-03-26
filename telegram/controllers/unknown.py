from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class UnknownHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text):
        self.reply(_("unknown"))
        self.user_session.state = 'main_menu'
        self.user_session.save()