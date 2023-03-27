from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _


class SettingsHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == _("back"):
            self.user_session.state = 'main_menu'
            self.user_session.save()
            return
        if text == _("change_language"):
            self.user_session.state = 'select_language'
            self.user_session.save()


class SettingsDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("choose_action"), keyboards.settings_keyboard())
