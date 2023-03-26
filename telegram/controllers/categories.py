from telegram.control import Control, Handler, Displayer
from telegram import keyboards

from django.utils.translation import gettext as _
from django.db.models import Q

from product.models import Category


class CategoriesHandler(Handler):
    def __init__(self, control: Control):
        super().__init__(control)

    def handle(self, text):
        if text == _("back"):
            self.user_session.state = 'main_menu'
            self.user_session.save()
            return
        category = Category.objects.filter(
            Q(name_uz=text) | Q(name_ru=text)).first()
        if category is None:
            self.reply(_("unknown"))
            return
        self.user_session.category = category
        self.user_session.state = 'products'
        self.user_session.save()


class CategoriesDisplayer(Displayer):
    def __init__(self, control: Control):
        super().__init__(control)

    def show(self):
        categories = Category.objects.all()
        self.reply(_("categories"), keyboards.categories_menu(
            categories, self.user.language))
