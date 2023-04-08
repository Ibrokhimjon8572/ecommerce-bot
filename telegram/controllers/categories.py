from telegram.control import Control, Handler, Displayer
from telegram import keyboards
from django.utils.translation import gettext as _
from django.db.models import Q

from product.models import Category


class CategoriesHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text, message_id=None):
        if text == _("back"):
            if self.user_session.category.parent is None:
                self.user_session.state = 'main_menu'
                self.user_session.category = None
                self.user_session.save()
                return
            self.user_session.category = self.user_session.category.parent
            self.user_session.save()
            return
        if text == _("basket"):
            self.user_session.state = 'basket'
            self.user_session.save()
            return
        category = Category.objects.filter(
            Q(name_uz=text) | Q(name_ru=text)).first()
        if category is None:
            self.reply(_("unknown"))
            return
        if category.is_product_category:
            self.user_session.category = category
            self.user_session.state = 'products'
            self.user_session.save()
            return
        category = Category.objects.get(
            Q(parent=self.user_session.category) & (Q(name_uz=text) | Q(name_ru=text)))
        self.user_session.category = category
        self.user_session.save()


class CategoriesDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        category = self.user_session.category
        if category:
            categories = Category.objects.filter(
                parent=category)
        else:
            categories = Category.objects.filter(parent=None)
        if category and category.image and category.image.url:
            caption = category.description_ru if self.user.language == 'ru' else category.description_uz
            name = category.name_ru if self.user.language == 'ru' else category.name_uz
            self.reply_image(
                self.base_url + category.image.url, caption or name)
        self.reply(_("categories"), keyboards.categories_menu(
            categories, self.user.language))
