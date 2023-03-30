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
from .send_comment import *
from .add_address import *
from .address_name import *
from .select_from_addresses import *
from .choose_payment import *
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
        case 'send_comment':
            return SendCommentHandler(control)
        case 'add_address':
            return AddAddressHandler(control)
        case 'address_name':
            return AddressNameHandler(control)
        case 'select_from_addresses':
            return SelectFromAddressesHandler(control)
        case 'choose_payment':
            return ChoosePaymentHandler(control)

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
        case 'send_comment':
            return SendCommentDisplayer(control)
        case 'add_address':
            return AddAddressDisplayer(control)
        case 'address_name':
            return AddressNameDisplayer(control)
        case 'select_from_addresses':
            return SelectFromAddressesDisplayer(control)
        case 'choose_payment':
            return ChoosePaymentDisplayer(control)

        case other:
            return MainMenuDisplayer(control)
