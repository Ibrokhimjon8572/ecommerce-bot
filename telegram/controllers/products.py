from telegram.control import Control, Handler, Displayer
from telegram import keyboards

from django.utils.translation import gettext as _
from django.db.models import Q
import logging
from product.models import Product


class ProductsHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text):
        if text == _("back"):
            self.user_session.state = 'categories'
            self.user_session.category = None
            self.user_session.save()
            return
        product = Product.objects.filter(
            Q(category=self.user_session.category) &
            (Q(name_uz=text) | Q(name_ru=text))).first()
        if product is None:
            self.reply(_("unknown"))
            return
        self.user_session.product = product
        self.user_session.state = 'amount'
        self.user_session.save()


class ProductsDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        category = self.user_session.category
        products = Product.objects.filter(category=category)
        caption = category.description_ru if self.user.language == 'ru' else category.description_uz
        name = category.name_ru if self.user.language == 'ru' else category.name_uz
        keyboard = keyboards.products_menu(products, self.user.language)
        if category.image.url:
            self.reply_image(
                self.base_url + category.image.url, caption, keyboard)
        else:
            self.reply(caption or name, keyboard)
