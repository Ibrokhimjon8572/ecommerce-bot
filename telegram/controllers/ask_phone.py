from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class AskPhoneHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def valid(self, phone):
        reg = RegexValidator(regex=r'^\+?998?\d{9}$', message="Not valid")
        try:
            reg(phone)
            return True
        except ValidationError:
            return False

    def handle(self, text, message_id=None):
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
