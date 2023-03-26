from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class StartHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text):
        self.user_session.state = "ask_phone"
        self.user_session.save()
