from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
import logging


class SelectFromAddressesHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == _("back"):
            self.user_session.state = 'order'
            self.user_session.save()
            return
        if text == _("add new address"):
            self.user_session.state = 'add_address'
            self.user_session.save()
            return
        try:
            address = self.user.addresses.get(name=text)
            self.user_session.lat = address.lat
            self.user_session.long = address.long
            self.user_session.state = 'send_comment'
            self.user_session.save()
        except Exception as e:
            logging.error(e)
            self.reply(_("unknown"))


class SelectFromAddressesDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        addresses = self.user.addresses.all()
        self.reply(_("select address"),
                   keyboards.select_address_keyboard(addresses))
