from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class MainMenuHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == _("orders"):
            self.user_session.state = 'categories'
            self.user_session.save()
        elif text == _("basket"):
            self.user_session.state = 'basket'
            self.user_session.save()
        else:
            self.reply(_("unknown"))


class MainMenuDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("main_menu"), keyboards.main_menu())
