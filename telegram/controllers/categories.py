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
        if self.user_session.category:
            categories = Category.objects.filter(
                parent=self.user_session.category)
        else:
            categories = Category.objects.filter(parent=None)
        self.reply(_("categories"), keyboards.categories_menu(
            categories, self.user.language))
