from telegram.control import Control, Handler


class StartHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        self.user_session.state = "ask_phone"
        self.user_session.save()
