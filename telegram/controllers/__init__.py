from telegram.control import Control, Handler, Displayer

from .start import *
from .ask_phone import *
from .main_menu import *
from .categories import *
from .products import *
from .amount import *
from .basket import *
from .settings import *
from .select_language import *
from .order import *
from .confirm_order import *
from .group_handler import *
from .unknown import *


def get_handler(control: Control, from_group=False) -> Handler:
    if from_group:
        return GroupHandler(control)
    match control.user_session.state:
        case 'start':
            return StartHandler(control)
        case 'ask_phone':
            return AskPhoneHandler(control)
        case 'main_menu':
            return MainMenuHandler(control)
        case 'categories':
            return CategoriesHandler(control)
        case 'products':
            return ProductsHandler(control)
        case 'amount':
            return AmountHandler(control)
        case 'basket':
            return BasketHandler(control)
        case 'settings':
            return SettingsHandler(control)
        case 'select_language':
            return SelectLanguageHandler(control)
        case 'order':
            return OrderHandler(control)
        case 'confirm_order':
            return ConfirmOrderHandler(control)

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
        case 'products':
            return ProductsDisplayer(control)
        case 'amount':
            return AmountDisplayer(control)
        case 'basket':
            return BasketDisplayer(control)
        case 'settings':
            return SettingsDisplayer(control)
        case 'select_language':
            return SelectLanguageDisplayer(control)
        case 'order':
            return OrderDisplayer(control)
        case 'confirm_order':
            return ConfirmOrderDisplayer(control)

        case other:
            return MainMenuDisplayer(control)
