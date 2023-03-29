from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
from telegram.models import UserAddress


class AddressNameHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, msg, message_id=None):
        if msg == _("back"):
            self.user_session.state = 'add_address'
            self.user_session.save()
            return
        address = UserAddress(
            user=self.user, lat=self.user_session.lat, long=self.user_session.long, name=msg)
        address.save()
        self.user_session.state = 'select_from_addresses'
        self.user_session.save()


class AddressNameDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        self.reply(_("enter address name"), keyboards.back())
