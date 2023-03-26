from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class AskPhoneHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def valid(self, phone):
        # TODO: add phone validator
        return True

    def handle(self, text):
        if self.user_session.state == "ask_phone":
            if not self.valid(text):
                self.reply(_("invalid_phone"))
                return
            self.user.phone = text
            self.user.save()
            self.user_session.state = "main_menu"
            self.user_session.save()


class AskPhoneDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("hello_message"), keyboards.send_phone())
