from telebot import types
from .control import bot, Control, ADMIN_GROUP
from .controllers import get_handler, get_displayer
from .controllers.payment_handler import PaymentHandler
from .controllers.report_handler import ReportHandler
from django.utils.translation import gettext as _
import logging


@bot.message_handler(commands=['start'])
def handle_start(msg: types.Message):
    if msg.from_user.id != msg.chat.id:
        return
    control = Control(msg.from_user)
    control.user_session.state = 'main_menu'
    if not control.user.phone:
        control.user_session.state = 'start'
    control.user_session.save()
    get_handler(control).handle(msg.text)
    get_displayer(control).show()


@bot.message_handler(commands=['report'])
def handle_report(msg: types.Message):
    if str(msg.chat.id) != ADMIN_GROUP:
        logging.error(msg)
        return
    control = Control(msg.from_user)
    ReportHandler(control).handle(msg)


@bot.message_handler(content_types=['contact'])
def handle_contact(msg: types.Message):
    if msg.from_user.id != msg.chat.id:
        return
    control = Control(msg.from_user)
    get_handler(control).handle(msg.contact.phone_number)
    get_displayer(control).show()


@bot.message_handler(content_types=['text'])
def handle_text(msg: types.Message):
    if msg.from_user.id != msg.chat.id:
        return
    control = Control(msg.from_user)
    if not control.user.phone and control.user_session.state != 'ask_phone':
        control.user_session.state = 'start'
        control.user_session.save()
    get_handler(control).handle(msg.text)
    get_displayer(control).show()


@bot.callback_query_handler(lambda _: True)
def handle_callback_query(cq: types.CallbackQuery):
    bot.answer_callback_query(cq.id)
    control = Control(cq.from_user)
    if cq.from_user.id != cq.message.chat.id:
        get_handler(control, from_group=True).handle(cq)
        return

    old_state = control.user_session.state
    get_handler(control).handle(cq.data, cq.message.id)
    if old_state != control.user_session.state:
        bot.delete_message(cq.message.chat.id, cq.message.id)
        get_displayer(control).show()


@bot.message_handler(content_types=['location'])
def handle_location(msg: types.Message):
    control = Control(msg.from_user)
    get_handler(control).handle(msg.location)
    get_displayer(control).show()


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query: types.PreCheckoutQuery):
    control = Control(pre_checkout_query.from_user)
    control.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=PaymentHandler(control).valid(pre_checkout_query),
                                          error_message=_("unknown"))


@bot.message_handler(content_types=['successful_payment'])
def handle_payment(msg: types.Message):
    control = Control(msg.from_user)
    PaymentHandler(control).handle(msg.successful_payment)
