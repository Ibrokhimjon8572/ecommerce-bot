from telegram.control import Control, Handler, Displayer

from .start import *
from .ask_phone import *
from .main_menu import *
from .categories import *
from .unknown import *


def get_handler(control: Control) -> Handler:
    match control.user_session.state:
        case 'start':
            return StartHandler(control)
        case 'ask_phone':
            return AskPhoneHandler(control)
        case 'main_menu':
            return MainMenuHandler(control)
        case 'categories':
            return CategoriesHandler(control)

        case other:
            return UnknownHandler(control)


def get_displayer(control: Control) -> Displayer:
    match control.user_session.state:
        case 'ask_phone':
            return AskPhoneDisplayer(control)
        case 'main_menu':
            return MainMenuDisplayer(control)
        case 'categories':
            return CategoriesDisplayer(control)

        case other:
            return MainMenuDisplayer(control)
