from telegram.control import Control, Handler, Displayer
from telegram import keyboards

from django.utils.translation import gettext as _
from order.models import OrderItem


class AmountHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == _("back"):
            self.user_session.state = 'products'
            self.user_session.amount = 0
            self.user_session.product = None
            self.user_session.save()
            return
        if text == _("basket"):
            self.user_session.state = 'basket'
            self.user_session.save()
            return
        try:
            amount = int(text)
            if amount <= 0:
                raise ValueError()
            order_item, _created = OrderItem.objects.get_or_create(
                order=self.order,
                product=self.user_session.product,
                defaults={
                    "price": self.user_session.product.price,
                }
            )
            order_item.amount = amount
            order_item.save()
            self.reply(_("added to basket"))
            self.user_session.state = 'categories'
            self.user_session.category = None
            self.user_session.product = None
            self.user_session.save()
        except:
            self.reply(_("invalid number"))


class AmountDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        product = self.user_session.product
        description = product.description_ru if self.user.language == "ru" else product.description_uz
        name = product.name_ru if self.user.language == "ru" else product.name_uz
        caption = _("%(description)s Price: %(price)d") % {
            "description": description or name, "price": product.price}
        if product.image and product.image.url:
            self.reply_image(
                self.base_url + product.image.url, caption, None)
        else:
            self.reply(caption, None)

        self.reply(_("choose"), keyboards.choose_keyboard())
