from telegram.control import Control, Handler, Displayer

from .ask_phone import *
from .main_menu import *
from .unknown import *


def get_handler(control: Control) -> Handler:
    match control.user_session.state:
        case 'ask_phone':
            return AskPhoneHandler(control)
        case 'main_menu':
            return MainMenuHandler(control)

        case other:
            return UnknownHandler(control)


def get_displayer(control: Control) -> Displayer:
    match control.user_session.state:
        case 'ask_phone':
            return AskPhoneDisplayer(control)
        case 'main_menu':
            return MainMenuDisplayer(control)

        case other:
            return MainMenuDisplayer(control)
