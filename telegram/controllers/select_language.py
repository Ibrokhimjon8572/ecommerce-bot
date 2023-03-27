from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
from django.utils import translation


class SelectLanguageHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == _("back"):
            self.user_session.state = 'settings'
            self.user_session.save()
            return
        if text == _("uz"):
            self.user.language = 'uz'
            translation.activate("uz")
            self.user.save()
        elif text == _("ru"):
            self.user.language = 'ru'
            translation.activate("ru")
            self.user.save()
        else:
            return
        self.reply(_("ready"))
        self.user_session.state = 'main_menu'
        self.user_session.save()


class SelectLanguageDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("choose_action"), keyboards.choose_language())
